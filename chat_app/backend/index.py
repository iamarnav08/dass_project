# app.py
from flask import Flask, request, jsonify, Response, stream_with_context, redirect
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import datetime
import os
from dotenv import load_dotenv
import re
import json
import sys
import pytz
import requests  # Add this import for HTTP requests
from urllib.parse import urlencode
import html

from retrieval import Generator
from quick_start_ncert_agent import NCERTGenerator
from test_generation import TestGenerator, set_collections, generate_and_save_test, evaluate_test_answers, get_user_tests, get_test_by_id
from encryption import EncryptionManager

load_dotenv()
chat_ollama = NCERTGenerator()

# Timezone configuration
IST = pytz.timezone('Asia/Kolkata')

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')  # Change in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://username:password@cluster.mongodb.net/userdb')
try:
    client = MongoClient(MONGO_URI, tz_aware=True)
    db = client.get_database('app_info')
    users_collection = db.users
    chats_collection = db.chats
    tests_collection = db.tests
    test_attempts_collection = db.test_attempts
    encryption_manager = EncryptionManager(MONGO_URI)
    
    # Initialize the test collections
    set_collections(tests_collection, test_attempts_collection)
    
    # Test connection
    client.admin.command('ping')
    print("MongoDB connection successful")
except Exception as e:
    print(f"MongoDB connection error: {e}")
    if 'encryption_manager' in locals():
        encryption_manager.close()
    exit(1)

# Add Google OAuth configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:3000/api/auth/callback/google')
GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_TOKEN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'


def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def validate_user(user_data):
    errors = []
    
    required_fields = ['username', 'email', 'password', 'grade']
    for field in required_fields:
        if field not in user_data:
            errors.append(f"Missing required field: {field}")
    
    if 'email' in user_data and not validate_email(user_data['email']):
        errors.append("Invalid email format")
    
    if 'password' in user_data and len(user_data['password']) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if 'grade' in user_data and user_data['grade'] not in ['10', '11', '12']:
        errors.append("Grade must be 10, 11, or 12")
        
    return errors

def sanitize_input(value):
    """
    Basic sanitation: escape HTML, strip leading/trailing whitespace,
    and prevent MongoDB operator injection.
    """
    if isinstance(value, str):
        value = value.strip()
        value = html.escape(value)
        # Prevent MongoDB operator injection
        if value.startswith('$'):
            value = value.replace('$', '')
        if '.' in value:
            value = value.replace('.', '')
    return value

def sanitize_dict(d, allowed_fields=None):
    """
    Sanitize all string values in a dict. Optionally restrict to allowed fields.
    """
    if not isinstance(d, dict):
        return d
    sanitized = {}
    for k, v in d.items():
        if allowed_fields and k not in allowed_fields:
            continue
        if isinstance(v, str):
            sanitized[k] = sanitize_input(v)
        elif isinstance(v, list):
            sanitized[k] = [sanitize_input(i) if isinstance(i, str) else i for i in v]
        else:
            sanitized[k] = v
    return sanitized

# Google OAuth routes
@app.route('/auth/google', methods=['GET'])
def google_auth():
    """
    Initiate the Google OAuth flow
    """
    auth_params = {
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': GOOGLE_REDIRECT_URI,
        'scope': 'email profile',
        'response_type': 'code',
        'access_type': 'offline',
        'prompt': 'consent'
    }
    
    auth_url = f"{GOOGLE_AUTH_URL}?{urlencode(auth_params)}"
    return jsonify({"auth_url": auth_url})

@app.route('/auth/google/callback', methods=['POST'])
def google_callback():
    """
    Handle the Google OAuth callback
    """
    try:
        # Get authorization code from frontend
        auth_code = request.json.get('code')
        
        if not auth_code:
            print("Error: No authorization code provided")
            return jsonify({"success": False, "message": "Authorization code is required"}), 400
        
        # Clean the auth code (remove potential URL encoding but preserve plus signs)
        auth_code = auth_code.replace(' ', '+')
        
        # Store a truncated version of the code for logging (avoid logging full codes)
        code_prefix = auth_code[:10] if len(auth_code) > 10 else "short_code"
        print(f"Processing auth code starting with: {code_prefix}...")
        
        # Exchange code for tokens
        token_data = {
            'code': auth_code,
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'redirect_uri': GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code'
        }
        
        print(f"Google OAuth request - client_id: {GOOGLE_CLIENT_ID[:8]}..., redirect_uri: {GOOGLE_REDIRECT_URI}")
        
        # Make token exchange request
        try:
            # Use debug mode to see detailed request
            token_response = requests.post(
                GOOGLE_TOKEN_URL, 
                data=token_data,
                # Uncomment for debugging
                # verify=False
            )
            token_status = token_response.status_code
            print(f"Token response status: {token_status}")
            
            # Log the complete response for debugging
            print(f"Token response content: {token_response.text[:200]}...")
            
            # Check for failure cases
            if token_status != 200:
                error_message = "Unknown error"
                
                try:
                    token_json = token_response.json()
                    print(f"Token error response: {token_json}")
                    
                    if 'error' in token_json:
                        error_type = token_json.get('error')
                        error_desc = token_json.get('error_description', '')
                        print(f"OAuth error: {error_type}, description: {error_desc}")
                        
                        if error_type == 'invalid_grant':
                            if 'Code was already redeemed' in error_desc:
                                return jsonify({
                                    "success": False, 
                                    "message": "Authentication code was already used. Please try logging in again."
                                }), 400
                except Exception as parse_error:
                    print(f"Error parsing token response: {str(parse_error)}")
                    error_message = token_response.text[:200]  # Limit response text for logging
                
                return jsonify({
                    "success": False, 
                    "message": f"Failed to obtain access token: {error_message}"
                }), 400
            
            # Successfully received token response
            token_json = token_response.json()
            
            if 'access_token' not in token_json:
                error_msg = token_json.get('error_description', token_json.get('error', 'Unknown error'))
                print(f"Error getting access token: {error_msg}")
                return jsonify({"success": False, "message": f"Failed to obtain access token: {error_msg}"}), 400
                
            access_token = token_json['access_token']
            print(f"Successfully obtained access token, length: {len(access_token)}")
            
        except Exception as token_error:
            print(f"Error making token request: {str(token_error)}")
            return jsonify({"success": False, "message": f"Token exchange error: {str(token_error)}"}), 500
            
        # Proceed with user info request using the access token
        try:
            user_info_response = requests.get(
                GOOGLE_USER_INFO_URL,
                headers={'Authorization': f'Bearer {access_token}'}
            )
            
            print(f"User info response status: {user_info_response.status_code}")
            if user_info_response.status_code != 200:
                print(f"Error getting user info: {user_info_response.text}")
                return jsonify({
                    "success": False, 
                    "message": f"Failed to get user info: {user_info_response.text}"
                }), 400
                
            user_info = user_info_response.json()
            print(f"User info: email={user_info.get('email')}, name={user_info.get('name')}")
        except Exception as user_info_error:
            print(f"Error getting user info: {str(user_info_error)}")
            return jsonify({"success": False, "message": f"User info error: {str(user_info_error)}"}), 500
        
        if 'email' not in user_info:
            print(f"Error: No email in user info: {user_info}")
            return jsonify({"success": False, "message": "Failed to get user email"}), 400
        
        user = users_collection.find_one({"email": user_info['email']})
        
        if not user:
            # Create new user
            username = user_info.get('name', '').replace(' ', '') or user_info['email'].split('@')[0]
            base_username = username
            
            counter = 1
            while users_collection.find_one({"username": username}):
                username = f"{base_username}{counter}"
                counter += 1
            
            # Set default grade to '10'
            grade = '10'
            
            # Create user
            new_user = {
                'email': user_info['email'],
                'username': username,
                'full_name': user_info.get('name', ''),
                'profile_picture': user_info.get('picture', ''),
                'google_id': user_info.get('sub', ''),
                'created_at': datetime.datetime.now(IST),
                'grade': grade,
                'last_active_date': None,
                'current_streak': 0,
                'longest_streak': 0,
                'streak_history': [],
                'auth_provider': 'google'
            }
            
            result = users_collection.insert_one(new_user)
            user_id = str(result.inserted_id)
            user_data = new_user
            user_data['_id'] = user_id
        else:
            # Update existing user with Google info
            users_collection.update_one(
                {"_id": user['_id']},
                {"$set": {
                    "google_id": user_info.get('sub', ''),
                    "profile_picture": user_info.get('picture', ''),
                    "auth_provider": "google"
                }}
            )
            user_id = str(user['_id'])
            # Get updated user data
            user_data = users_collection.find_one({"_id": ObjectId(user_id)})
            user_data['_id'] = user_id
        
        # Remove sensitive data
        if 'password' in user_data:
            del user_data['password']
        
        # Create JWT token
        access_token = create_access_token(identity=user_id)
        
        return jsonify({
            "success": True,
            "access_token": access_token,
            "user": user_data,
            "message": "Google login successful"
        })
        
    except Exception as e:
        print(f"Google auth error: {str(e)}")
        return jsonify({"success": False, "message": f"Authentication failed: {str(e)}"}), 500


@app.route('/register', methods=['POST'])
def register():
    user_data = request.json

    # Sanitize input
    user_data = sanitize_dict(user_data, allowed_fields=['username', 'email', 'password', 'grade'])

    validation_errors = validate_user(user_data)
    if (validation_errors):
        return jsonify({"success": False, "errors": validation_errors}), 400

    # Check if user already exists
    if users_collection.find_one({"email": user_data['email']}):
        return jsonify({"success": False, "message": "Email already registered"}), 409
    
    if users_collection.find_one({"username": user_data['username']}):
        return jsonify({"success": False, "message": "Username already taken"}), 409
    
    # Hash password
    user_data['password'] = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
    
    # Add created_at timestamp
    user_data['created_at'] = datetime.datetime.now(IST)
    
    # Add default values for Streak and other fields
    user_data['last_active_date'] = None
    user_data['current_streak'] = 0
    user_data['longest_streak'] = 0
    user_data['streak_history'] = []
    
    # Insert user into the database
    result = users_collection.insert_one(user_data)
    
    # Create token
    access_token = create_access_token(identity=str(result.inserted_id))
    
    return jsonify({
        "success": True,
        "message": "User registered successfully",
        "user_id": str(result.inserted_id),
        "access_token": access_token
    }), 201

@app.route('/login', methods=['POST'])
def login():
    login_data = request.json

    # Sanitize input
    login_data = sanitize_dict(login_data, allowed_fields=['email', 'username', 'password'])

    # Check if email/username and password are provided
    if not login_data or 'password' not in login_data:
        return jsonify({"success": False, "message": "Missing login credentials"}), 400
    
    # Find user by email or username
    user = None
    if 'email' in login_data:
        user = users_collection.find_one({"email": login_data['email']})
    elif 'username' in login_data:
        user = users_collection.find_one({"username": login_data['username']})
    else:
        return jsonify({"success": False, "message": "Email or username required"}), 400
    
    # Verify user exists and password is correct
    if not user or not bcrypt.check_password_hash(user['password'], login_data['password']):
        return jsonify({"success": False, "message": "Invalid credentials"}), 401
    
    # Create token
    access_token = create_access_token(identity=str(user['_id']))
    
    return jsonify({
        "success": True,
        "message": "Login successful",
        "access_token": access_token
    }), 200

@app.route('/user', methods=['GET'])
@jwt_required()
def get_user_profile():
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Find user in database
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    
    # Remove sensitive data
    user.pop('password', None)
    user['_id'] = str(user['_id'])
    
    # Include streak information
    streak_data = {
        'current_streak': user.get('current_streak', 0),
        'longest_streak': user.get('longest_streak', 0),
        'streak_history': user.get('streak_history', []),
        'last_active_date': user.get('last_active_date')
    }
    user['streak_data'] = streak_data
    
    return jsonify({
        "success": True,
        "user": user
    }), 200

@app.route('/user', methods=['PUT'])
@jwt_required()
def update_user():
    user_id = get_jwt_identity()
    update_data = request.json

    # Fetch the existing user from the database
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    # Check if the new username is the same as the existing one
    if 'username' in update_data and update_data['username'] == user['username']:
        return jsonify({"success": False, "message": "The new username is the same as the existing username"}), 400

    # Don't allow email or username updates (or handle them specially)
    if 'email' in update_data:
        return jsonify({"success": False, "message": "Email cannot be updated"}), 400

    if 'username' in update_data:
        # Check if the new username is already taken
        if users_collection.find_one({"username": update_data['username']}):
            return jsonify({"success": False, "message": "Username already taken"}), 409

    # Update the user data
    users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    return jsonify({"success": True, "message": "User updated successfully"}), 200

@app.route('/user', methods=['DELETE'])
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()
    
    # Delete user from database
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    
    if result.deleted_count == 0:
        return jsonify({"success": False, "message": "User not found"}), 404
    
    return jsonify({
        "success": True,
        "message": "User deleted successfully"
    }), 200

# Store blacklisted tokens
blacklist = set()

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Get the current token
    jti = get_jwt()["jti"]  # JTI (JWT ID) is a unique identifier for the token
    blacklist.add(jti)  # Add the token to the blacklist
    return jsonify({"success": True, "message": "Logout successful"}), 200

# Update JWTManager to check for blacklisted tokens
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in blacklist

@app.route('/generate', methods=['POST'])
@jwt_required()
def generate_text():
    user_id = get_jwt_identity()
    data = request.json
    complete_response = []
    full_response = ""

    required_fields = ['grade', 'subjects', 'query']
    if not all(field in data for field in required_fields):
        return jsonify({
            "success": False, 
            "message": "Missing required fields"
        }), 400
    
    conversation_id = data.get('conversation_id')
    is_new_conversation = False
    current_time = datetime.datetime.now(IST)

    actual_conversation_id = conversation_id
    
    if not conversation_id:
        # Create a new conversation right away 
        is_new_conversation = True
        try:
            # Create new conversation with empty bot response
            conversation = {
                'user_id': ObjectId(user_id),
                'created_at': current_time,
                'last_updated': current_time,
                'name': format(current_time, '%B %d, %Y'),
                'grade': data.get('grade'),
                'subjects': data.get('subjects'),
                'messages': [{
                    'user_input': encryption_manager.encrypt_field(data.get('query')),
                    'bot_response': encryption_manager.encrypt_field(""),  # Empty initially
                    'timestamp': current_time
                }]
            }
            
            result = chats_collection.insert_one(conversation)
            actual_conversation_id = str(result.inserted_id)
            print(f"Created new conversation with ID: {actual_conversation_id}")
        except Exception as e:
            print(f"Error creating new conversation: {str(e)}")
    
    def generate():
        nonlocal full_response
        try:
            yield "data: {\"status\":\"start\"}\n\n"
            
            # Create a thread metadata object with the user ID
            thread_metadata = {"user_id": user_id}
            
            # Pass conversation_id and metadata to the generator
            for chunk in chat_ollama.generate(
                data['grade'],
                data['subjects'],
                data['query'],
                conversation_id=actual_conversation_id,  # Pass the conversation ID for context
                store_messages=False,  # Disable storing messages in EphemeralMemory
                thread_metadata=thread_metadata  # Pass user_id in thread metadata
            ):
                complete_response.append(chunk)
                print(".", end="", flush=True)
                chunk_json = json.dumps({'chunk': chunk})
                yield f"data: {chunk_json}\n\n"
                # Force flush to ensure chunks are sent immediately
                sys.stdout.flush()

            full_response = ''.join(complete_response)
            
            # Send explicit completion signal
            done_signal = json.dumps({
                'done': True, 
                'conversation_id': actual_conversation_id,
                'is_new_conversation': is_new_conversation
            })
            print("Sending completion signal:", done_signal)
            yield f"data: {done_signal}\n\n"
            sys.stdout.flush()
            
            # Update the conversation in MongoDB with the query and response
            if actual_conversation_id:
                print(f"Updating conversation {actual_conversation_id} with response")
                
                if is_new_conversation:
                    # For new conversations, we already added the message, just update the response
                    conversation = chats_collection.find_one({'_id': ObjectId(actual_conversation_id)})
                    
                    if conversation and conversation.get('messages'):
                        # Get the timestamp of the last message for targeting
                        last_timestamp = conversation['messages'][-1]['timestamp']
                        
                        # Update the bot response
                        result = chats_collection.update_one(
                            {'_id': ObjectId(actual_conversation_id)},
                            {
                                '$set': {
                                    'messages.$[last].bot_response': encryption_manager.encrypt_field(full_response)
                                }
                            },
                            array_filters=[{'last.timestamp': last_timestamp}]
                        )
                        
                        print(f"MongoDB update result: {result.modified_count} documents modified")
                    else:
                        print("Warning: Could not find conversation or it has no messages")
                else:
                    result = chats_collection.update_one(
                        {'_id': ObjectId(actual_conversation_id)},
                        {
                            '$set': {'last_updated': current_time}
                        }
                    )
                    print(f"Updated timestamp for existing conversation: {result.modified_count} documents modified")
                
        except Exception as e:
            error_msg = f"Error in generate(): {str(e)}"
            print(error_msg)
            yield f"data: {json.dumps({'error': error_msg})}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
            'Content-Type': 'text/event-stream',
            'Connection': 'keep-alive'
        }
    )


@app.route('/api/user/username', methods=['PUT'])
@jwt_required()
def update_username():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        new_username = data.get('username')

        if not new_username:
            return jsonify({'message': 'Username is required'}), 400

        # Check if username is already taken
        existing_user = users_collection.find_one({"username": new_username})
        if existing_user and str(existing_user['_id']) != current_user_id:
            return jsonify({'message': 'Username is already taken'}), 400

        # Update username
        users_collection.update_one(
            {"_id": ObjectId(current_user_id)},
            {"$set": {"username": new_username}}
        )

        return jsonify({'message': 'Username updated successfully'}), 200
    except Exception as e:
        print(f"Error updating username: {str(e)}")
        return jsonify({'message': 'Failed to update username'}), 500

@app.route('/api/user/password', methods=['PUT'])
@jwt_required()
def update_password():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if not current_password or not new_password:
            return jsonify({'message': 'Current password and new password are required'}), 400

        # Get user and verify current password
        user = users_collection.find_one({"_id": ObjectId(current_user_id)})
        if not user or not bcrypt.check_password_hash(user['password'], current_password):
            return jsonify({'message': 'Current password is incorrect'}), 401

        # Validate new password
        if len(new_password) < 8:
            return jsonify({'message': 'New password must be at least 8 characters long'}), 400

        # Update password
        users_collection.update_one(
            {"_id": ObjectId(current_user_id)},
            {"$set": {"password": bcrypt.generate_password_hash(new_password).decode('utf-8')}}
        )

        return jsonify({'message': 'Password updated successfully'}), 200
    except Exception as e:
        print(f"Error updating password: {str(e)}")
        return jsonify({'message': 'Failed to update password'}), 500

@app.route('/api/user/grade', methods=['PUT'])
@jwt_required()
def update_grade():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        new_grade = data.get('grade')

        if not new_grade:
            return jsonify({'message': 'Grade is required'}), 400

        # Validate grade
        if new_grade not in ['10', '11', '12']:
            return jsonify({'message': 'Grade must be 10, 11, or 12'}), 400

        # Update grade
        users_collection.update_one(
            {"_id": ObjectId(current_user_id)},
            {"$set": {"grade": new_grade}}
        )

        return jsonify({'message': 'Grade updated successfully'}), 200
    except Exception as e:
        print(f"Error updating grade: {str(e)}")
        return jsonify({'message': 'Failed to update grade'}), 500

# User activity tracking
@app.route('/api/user/activity', methods=['POST'])
@jwt_required()
def update_user_activity():
    user_id = get_jwt_identity()
    today = datetime.datetime.now(IST).date()
    
    # Find user in database
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    
    # Get the last active date (if any)
    last_active_date = user.get('last_active_date')
    if (last_active_date):
        last_active = datetime.datetime.fromisoformat(last_active_date)
        if not last_active.tzinfo:
            last_active = IST.localize(last_active)
        last_active = last_active.date()
        
        # Calculate streak
        if last_active == today:
            # Already counted for today
            pass
        elif (today - last_active).days == 1:
            # Consecutive day - increase streak
            users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$inc": {"current_streak": 1}}
            )
        else:
            # Streak broken - reset to 1
            users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"current_streak": 1}}
            )
    else:
        # First activity - start streak at 1
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"current_streak": 1}}
        )
    
    # Update last_active_date
    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {
            "$set": {"last_active_date": today.isoformat()},
            "$addToSet": {"streak_history": today.isoformat()}
        }
    )
    
    # Update longest streak if current streak is longer
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user['current_streak'] > user.get('longest_streak', 0):
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"longest_streak": user['current_streak']}}
        )
    
    return jsonify({
        "success": True,
        "current_streak": user['current_streak'],
        "longest_streak": max(user['current_streak'], user.get('longest_streak', 0))
    }), 200

# Clear user activity data
@app.route('/api/user/clear-activity', methods=['POST'])
@jwt_required()
def clear_activity():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        password = data.get('password')

        if not password:
            return jsonify({'message': 'Password is required'}), 400
            
        # Get user and verify password
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user or not bcrypt.check_password_hash(user['password'], password):
            return jsonify({'message': 'Incorrect password'}), 401
            
        # Clear streaks
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "current_streak": 0,
                    "longest_streak": 0,
                    "streak_history": []
                }
            }
        )
        
        # Delete all user's chats
        chats_collection.delete_many({"user_id": ObjectId(user_id)})
        
        # Delete all user's tests
        tests_collection.delete_many({"user_id": ObjectId(user_id)})
        
        # Delete all user's test attempts
        test_attempts_collection.delete_many({"user_id": ObjectId(user_id)})
        
        return jsonify({
            'success': True,
            'message': 'All activity data has been cleared successfully'
        }), 200
    except Exception as e:
        print(f"Error clearing activity data: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to clear activity data'}), 500

# For storing chats

@app.route('/api/chats', methods=['POST'])
@jwt_required()
def save_chat():
    try:
        user_id = get_jwt_identity()
        data = request.json
        
        # print(f"Received save request for user {user_id}")
        # print(f"Request data: {data}")
        
        # Get or create conversation
        conversation_id = data.get('conversation_id')
        current_time = datetime.datetime.now(IST)
        
        if conversation_id:
            # print(f"Updating existing conversation: {conversation_id}")
            # Update existing conversation
            result = chats_collection.update_one(
                {
                    '_id': ObjectId(conversation_id),
                    'user_id': ObjectId(user_id)
                },
                {
                    '$push': {
                        'messages': {
                            # 'user_input': data.get('user_input'),
                            # 'bot_response': data.get('bot_response'),
                            'user_input': encryption_manager.encrypt_field(data.get('user_input')),
                            'bot_response': encryption_manager.encrypt_field(data.get('bot_response')),
                            'timestamp': current_time
                        }
                    },
                    '$set': {
                        'last_updated': current_time
                    }
                }
            )
            # print(f"Update result: {result.modified_count} documents modified")
            conversation = chats_collection.find_one({'_id': ObjectId(conversation_id)})
        else:
            # print("Creating new conversation")
            # Create new conversation
            conversation = {
                'user_id': ObjectId(user_id),
                'created_at': current_time,
                'last_updated': current_time,
                'name': format(current_time, '%B %d, %Y'),
                'grade': data.get('grade'),
                'subjects': data.get('subjects'),
                'messages': [{
                    # 'user_input': data.get('user_input'),
                    # 'bot_response': data.get('bot_response'),
                    'user_input': encryption_manager.encrypt_field(data.get('user_input')),
                    'bot_response': encryption_manager.encrypt_field(data.get('bot_response')),
                    'timestamp': current_time
                }]
            }
            
            result = chats_collection.insert_one(conversation)
            conversation_id = str(result.inserted_id)
            # print(f"Created new conversation with ID: {conversation_id}")
            conversation = chats_collection.find_one({'_id': result.inserted_id})
        
        return jsonify({
            'success': True,
            'conversation_id': str(conversation_id),
            'name': conversation['name'],
            'created_at': conversation['created_at'].isoformat(),
            'last_updated': conversation['last_updated'].isoformat()
        }), 201
        
    except Exception as e:
        print(f"Error saving chat: {str(e)}")
        return jsonify({'success': False, 'message': f'Failed to save chat: {str(e)}'}), 500




@app.route('/api/chats', methods=['GET'])
@jwt_required()
def get_user_chats():
    try:
        user_id = get_jwt_identity()
        # print("getting chats for user id:", user_id)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        skip = (page - 1) * per_page
        total_conversations = chats_collection.count_documents({'user_id': ObjectId(user_id)})
        
        conversations = chats_collection.find(
            {'user_id': ObjectId(user_id)}
        ).sort('last_updated', -1).skip(skip).limit(per_page)
        
        conversation_list = []
        for conv in conversations:
            # Get last message for preview
            last_message = conv['messages'][-1] if conv['messages'] else None
            
            conversation_list.append({
                'conversation_id': str(conv['_id']),
                'name': conv.get('name'),
                'created_at': conv['created_at'].isoformat(),
                'last_updated': conv['last_updated'].isoformat(),
                'grade': conv['grade'],
                'subjects': conv['subjects'],
                'message_count': len(conv['messages']),
                'last_message': {
                    'user_input': encryption_manager.decrypt_field(last_message['user_input']),
                    'bot_response': encryption_manager.decrypt_field(last_message['bot_response']),
                    # 'user_input': last_message['user_input'],
                    # 'bot_response': last_message['bot_response'],
                    'timestamp': last_message['timestamp'].isoformat()
                } if last_message else None
            })
        
        return jsonify({
            'success': True,
            'conversations': conversation_list,
            'total': total_conversations,
            'page': page,
            'per_page': per_page,
            'total_pages': (total_conversations + per_page - 1) // per_page
        }), 200
        
    except Exception as e:
        print(f"Error retrieving conversations: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to retrieve conversations'}), 500
    

@app.route('/api/chats/<conversation_id>/messages', methods=['GET'])
@jwt_required()
def get_conversation_messages(conversation_id):
    try:
        user_id = get_jwt_identity()
        
        conversation = chats_collection.find_one({
            '_id': ObjectId(conversation_id),
            'user_id': ObjectId(user_id)
        })
        
        if not conversation:
            return jsonify({'success': False, 'message': 'Conversation not found'}), 404
            
        messages = []
        for msg in conversation['messages']:
            try:
                user_input = encryption_manager.decrypt_field(msg['user_input'])
                bot_response = encryption_manager.decrypt_field(msg['bot_response'])
            except Exception as e:
                print(f"Decryption error: {str(e)}. Using raw values.")
                user_input = msg['user_input']
                bot_response = msg['bot_response']
                
            messages.append({
                'user_input': user_input,
                'bot_response': bot_response,
                'timestamp': msg['timestamp'].isoformat() if isinstance(msg['timestamp'], datetime.datetime) else msg['timestamp']
            })
            
        return jsonify({
            'success': True,
            'conversation_id': conversation_id,
            'name': conversation['name'],
            'grade': conversation['grade'],
            'subjects': conversation['subjects'],
            'messages': messages
        }), 200
        
    except Exception as e:
        print(f"Error retrieving messages: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to retrieve messages'}), 500


@app.route('/api/chats/<chat_id>', methods=['GET'])
@jwt_required()
def get_chat_by_id(chat_id):
    try:
        user_id = get_jwt_identity()
        
        chat = chats_collection.find_one({
            '_id': ObjectId(chat_id),
            'user_id': ObjectId(user_id)
        })
        
        if not chat:
            return jsonify({'success': False, 'message': 'Chat not found'}), 404
        
        # The chat document structure is different than expected
        # It contains an array of messages, not direct user_input/bot_response fields
        try:
            # Format like get_conversation_messages
            messages = []
            for msg in chat.get('messages', []):
                try:
                    # Try to decrypt, but handle gracefully if it fails
                    user_input = encryption_manager.decrypt_field(msg['user_input'])
                    bot_response = encryption_manager.decrypt_field(msg['bot_response'])
                except Exception as e:
                    print(f"Decryption error: {str(e)}. Using raw values.")
                    user_input = msg['user_input']
                    bot_response = msg['bot_response']
                
                messages.append({
                    'user_input': user_input,
                    'bot_response': bot_response,
                    'timestamp': msg['timestamp'].isoformat() if isinstance(msg['timestamp'], datetime.datetime) else msg['timestamp']
                })
                
            return jsonify({
                'success': True,
                'chat': {
                    'chat_id': str(chat['_id']),
                    'name': chat.get('name', ''),
                    'created_at': chat['created_at'].isoformat() if isinstance(chat['created_at'], datetime.datetime) else chat['created_at'],
                    'last_updated': chat['last_updated'].isoformat() if isinstance(chat['last_updated'], datetime.datetime) else chat['last_updated'],
                    'grade': chat.get('grade'),
                    'subjects': chat.get('subjects', []),
                    'messages': messages
                }
            }), 200
        except Exception as format_error:
            print(f"Error formatting chat: {str(format_error)}")
            # Return a simplified response as fallback
            return jsonify({
                'success': True,
                'chat': {
                    'chat_id': str(chat['_id']),
                    'name': chat.get('name', ''),
                    'message_count': len(chat.get('messages', [])),
                }
            }), 200
            
    except Exception as e:
        print(f"Error retrieving chat: {str(e)}")
        return jsonify({'success': False, 'message': f'Failed to retrieve chat: {str(e)}'}), 500   

@app.route('/api/chats/<chat_id>/rename', methods=['PATCH'])
@jwt_required()
def rename_chat(chat_id):
    try:
        user_id = get_jwt_identity()
        data = request.json
        new_name = data.get('name')
        
        if not new_name:
            return jsonify({'success': False, 'message': 'New name is required'}), 400
            
        result = chats_collection.update_one(
            {
                '_id': ObjectId(chat_id),
                'user_id': ObjectId(user_id)
            },
            {
                '$set': {'name': new_name}
            }
        )
        
        if result.matched_count == 0:
            return jsonify({'success': False, 'message': 'Chat not found'}), 404
            
        return jsonify({
            'success': True,
            'message': 'Chat renamed successfully'
        }), 200
        
    except Exception as e:
        print(f"Error renaming chat: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to rename chat'}), 500

@app.route('/api/chats/<chat_id>', methods=['DELETE'])
@jwt_required()
def delete_chat(chat_id):
    try:
        user_id = get_jwt_identity()
        
        result = chats_collection.delete_one({
            '_id': ObjectId(chat_id),
            'user_id': ObjectId(user_id)
        })
        
        if result.deleted_count == 0:
            return jsonify({'success': False, 'message': 'Chat not found'}), 404
            
        return jsonify({
            'success': True,
            'message': 'Chat deleted successfully'
        }), 200
        
    except Exception as e:
        print(f"Error deleting chat: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to delete chat'}), 500

# Test Generation and Evaluation Routes

@app.route('/api/generate_test', methods=['POST'])
@jwt_required()
def generate_test():
    try:
        user_id = get_jwt_identity()
        data = request.json
        
        # Required fields
        required_fields = ['topic', 'grade', 'subjects', 'title']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'message': 'Missing required fields (topic, grade, subjects, title)'
            }), 400
        
        # Optional fields with defaults
        num_questions = int(data.get('num_questions', 5))
        
        # Generate and save the test
        result = generate_and_save_test(
            user_id=user_id,
            title=data['title'],
            topic=data['topic'],
            grade=data['grade'],
            subjects=data['subjects'],
            num_questions=num_questions
        )
        
        if not result['success']:
            return jsonify({
                'success': False,
                'message': f"Error generating test: {result['error']}"
            }), 500
        
        # Ensure the test ID is included in the test object itself
        test_data = result['test']
        test_data['_id'] = result['test_id']  # Add ID to the test object for frontend consistency
        
        # Return success response with the test data
        return jsonify({
            'success': True,
            'message': 'Test generated and saved successfully',
            'test_id': result['test_id'],
            'test': test_data
        }), 201
        
    except Exception as e:
        print(f"Error generating test: {str(e)}")
        return jsonify({
            'success': False, 
            'message': f'Failed to generate test: {str(e)}'
        }), 500

@app.route('/api/evaluate_test', methods=['POST'])
@jwt_required()
def evaluate_test():
    try:
        user_id = get_jwt_identity()
        data = request.json
        
        # Required fields
        required_fields = ['test_id', 'answers']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'message': 'Missing required fields (test_id, answers)'
            }), 400
        
        # Evaluate the test
        result = evaluate_test_answers(
            user_id=user_id,
            test_id=data['test_id'],
            answers=data['answers']
        )
        
        if not result['success']:
            return jsonify({
                'success': False,
                'message': result['error']
            }), 404
            
        # Extract the percentage score from the complex score object
        score_percentage = result['score']['percentage']
        
        # Update the test document with attempt count and best score
        test = tests_collection.find_one({'_id': ObjectId(data['test_id'])})
        current_attempts = test.get('attempts', 0) + 1
        current_best_score = test.get('best_score', 0)
        
        update_data = {
            'attempts': current_attempts,
            'last_attempt_score': score_percentage,
            'last_attempt_date': datetime.datetime.now(IST)
        }
        
        # Update best score if current score is higher
        if score_percentage > current_best_score:
            update_data['best_score'] = score_percentage
            
        tests_collection.update_one(
            {'_id': ObjectId(data['test_id'])},
            {'$set': update_data}
        )
        
        # Get previous attempts for this test
        previous_attempts = list(test_attempts_collection.find(
            {'user_id': ObjectId(user_id), 'test_id': ObjectId(data['test_id'])}
        ).sort('timestamp', -1).limit(5))
        
        # Format previous attempts for response
        attempt_history = []
        for attempt in previous_attempts:
            attempt_score = attempt.get('score', {})
            percentage = attempt_score.get('percentage', 0) if isinstance(attempt_score, dict) else attempt_score
            
            attempt_history.append({
                'score': percentage,
                'timestamp': attempt['timestamp'].isoformat(),
                'attempt_id': str(attempt['_id'])
            })
        
        # Return evaluation results with attempt history and simplified score
        return jsonify({
            'success': True,
            'test_title': result['test_title'],
            'test_topic': result['test_topic'],
            'evaluation': result['evaluation'],
            'score': score_percentage,  # Send percentage directly for frontend compatibility
            'score_details': result['score'],  # Also include the detailed score object
            'attempt_history': attempt_history,
            'best_score': update_data.get('best_score', current_best_score),
            'attempts_count': current_attempts
        }), 200
        
    except Exception as e:
        print(f"Error evaluating test: {str(e)}")
        return jsonify({
            'success': False, 
            'message': f'Failed to evaluate test: {str(e)}'
        }), 500

@app.route('/api/tests', methods=['GET'])
@jwt_required()
def get_all_tests():
    try:
        user_id = get_jwt_identity()
        
        # Pagination parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # Filtering parameters
        topic_filter = request.args.get('topic')
        grade_filter = request.args.get('grade')
        subject_filter = request.args.get('subject')
        
        # Get tests
        result = get_user_tests(
            user_id=user_id,
            page=page,
            per_page=per_page,
            topic_filter=topic_filter,
            grade_filter=grade_filter,
            subject_filter=subject_filter
        )
        
        # Ensure each test has a proper _id field (in addition to test_id)
        if result['success'] and 'tests' in result:
            for test in result['tests']:
                if 'test_id' in test and '_id' not in test:
                    test['_id'] = test['test_id']
                elif '_id' not in test and 'id' not in test:
                    # Fallback to ensure there's always an ID
                    test['_id'] = str(ObjectId())
        
        # Return the tests
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Error retrieving tests: {str(e)}")
        return jsonify({
            'success': False, 
            'message': f'Failed to retrieve tests: {str(e)}'
        }), 500

@app.route('/api/tests/<test_id>', methods=['GET'])
@jwt_required()
def get_test_by_id_route(test_id):
    try:
        user_id = get_jwt_identity()
        
        # Validate test_id to avoid MongoDB errors
        if not test_id or test_id == 'undefined' or test_id == 'null':
            error_msg = f"Invalid test ID: {test_id}"
            print(error_msg)
            return jsonify({
                'success': False,
                'message': 'Invalid test ID format'
            }), 400
        
        # Log the incoming test ID for debugging
        print(f"Fetching test with ID: {test_id}")
        
        # Check if answers should be shown
        show_answers = request.args.get('show_answers', 'false').lower() == 'true'
        
        # Get the test
        result = get_test_by_id(
            test_id=test_id,
            user_id=user_id,
            show_answers=show_answers
        )
        
        if not result['success']:
            error_msg = result['error']
            print(f"Error fetching test: {error_msg}")
            if error_msg == 'Invalid test ID format':
                return jsonify({'success': False, 'message': error_msg}), 400
            elif error_msg == 'Test not found':
                return jsonify({'success': False, 'message': error_msg}), 404
            else:
                return jsonify({'success': False, 'message': error_msg}), 403
        
        # Add _id field to the test for frontend consistency
        if 'test' in result and 'test_id' in result:
            result['test']['_id'] = result['test_id']
            
        # Fetch previous attempts for this test
        previous_attempts = list(test_attempts_collection.find(
            {'user_id': ObjectId(user_id), 'test_id': ObjectId(test_id)}
        ).sort('timestamp', -1).limit(10))
        
        # Format previous attempts for response
        attempt_history = []
        for attempt in previous_attempts:
            attempt_score = attempt.get('score', {})
            percentage = attempt_score.get('percentage', 0) if isinstance(attempt_score, dict) else attempt_score
            
            attempt_history.append({
                'score': percentage,
                'timestamp': attempt['timestamp'].isoformat(),
                'attempt_id': str(attempt['_id'])
            })
            
        # Add attempt history to the result
        if 'test' in result:
            result['test']['attempt_history'] = attempt_history
        
        # Return the test
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Error retrieving test: {str(e)}")
        return jsonify({
            'success': False, 
            'message': f'Failed to retrieve test: {str(e)}'
        }), 500

@app.route('/api/tests/<test_id>', methods=['DELETE'])
@jwt_required()
def delete_test(test_id):
    try:
        user_id = get_jwt_identity()
        
        # Validate test ID
        if not test_id or test_id == 'undefined' or test_id == 'null':
            return jsonify({
                'success': False,
                'message': 'Invalid test ID'
            }), 400
            
        # Check if test exists and belongs to user
        test = tests_collection.find_one({
            '_id': ObjectId(test_id),
            'user_id': ObjectId(user_id)
        })
        
        if not test:
            return jsonify({
                'success': False,
                'message': 'Test not found or you do not have permission to delete it'
            }), 404
            
        # Delete test
        tests_collection.delete_one({'_id': ObjectId(test_id)})
        
        # Delete associated test attempts
        test_attempts_collection.delete_many({'test_id': ObjectId(test_id)})
        
        return jsonify({
            'success': True,
            'message': 'Test deleted successfully'
        }), 200
        
    except Exception as e:
        print(f"Error deleting test: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Failed to delete test: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
