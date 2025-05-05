'use client';

import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { FiSend, FiUser, FiLogOut, FiMenu, FiX, FiMessageSquare, FiCheck, FiSettings, FiClipboard } from 'react-icons/fi';
import { authService } from '@/lib/auth';
import { format } from 'date-fns';
import { FiEdit2, FiTrash2 } from 'react-icons/fi';
import { FiChevronRight, FiChevronLeft } from 'react-icons/fi';  

interface Message {
  id: string;
  sender: string;
  content: string;
  timestamp: string;
}

interface Subject {
  code: string;
  name: string;
}

interface Conversation {
  _id: string;
  conversation_id?: string;
  name: string;
  timestamp: string;
  created_at?: string;
  last_updated?: string;
  grade?: string;
  subjects?: string[];
  message_count?: number;
  messages?: {
    user_input: string;
    bot_response: string;
    timestamp: string;
  }[];
  last_message?: {
    user_input: string;
    bot_response: string;
    timestamp: string;
  };
}

// Add grade and subject options
const GRADES = ["10", "11", "12"];
const SUBJECTS: Record<string, Subject[]> = {
  "10": [
    { code: "civics", name: "Civics" },
    { code: "eco", name: "Economics" },
    { code: "english", name: "English" },
    { code: "english2", name: "English Literature" },
    { code: "english3", name: "English Workbook" },
    { code: "geo", name: "Geography" },
    { code: "history", name: "History" },
    { code: "math", name: "Mathematics" },
    { code: "pe", name: "Health and Physical Education" },
    { code: "sci", name: "Science" }
  ],
  "11": [
    { code: "acc", name: "Accountancy" },
    { code: "acc2", name: "Accountancy-II" },
    { code: "art", name: "Fine Art" },
    { code: "bio", name: "Biology" },
    { code: "biotech", name: "Biotechnology" },
    { code: "bus", name: "Business Studies" },
    { code: "chem", name: "Chemistry" },
    { code: "comp", name: "Computer Science" },
    { code: "eco", name: "Economics" },
    { code: "eco2", name: "Statistics for Economics" },
    { code: "english", name: "English" },
    { code: "english2", name: "English Literature" },
    { code: "english3", name: "English Supplementary" },
    { code: "geo", name: "Geography" },
    { code: "geo2", name: "Practical Geography" },
    { code: "geo3", name: "Indian Geography" },
    { code: "history", name: "History" },
    { code: "home", name: "Home Science" },
    { code: "inf", name: "Informatics Practices" },
    { code: "kno", name: "Knowledge Tradition" },
    { code: "math", name: "Mathematics" },
    { code: "pe", name: "Health and Physical Education" },
    { code: "phy", name: "Physics" },
    { code: "pol", name: "Political Science" },
    { code: "pol2", name: "Indian Constitution" },
    { code: "psy", name: "Psychology" },
    { code: "soc", name: "Sociology" },
    { code: "soc2", name: "Understanding Society" }
  ],
  "12": [
    { code: "acc", name: "Accountancy" },
    { code: "acc2", name: "Accountancy-II" },
    { code: "acc3", name: "Computerized Accounting" },
    { code: "art", name: "Fine Art" },
    { code: "bio", name: "Biology" },
    { code: "biotech", name: "Biotechnology" },
    { code: "bus", name: "Business Studies" },
    { code: "chem", name: "Chemistry" },
    { code: "comp", name: "Computer Science" },
    { code: "eco", name: "Microeconomics" },
    { code: "eco2", name: "Macroeconomics" },
    { code: "english", name: "English" },
    { code: "english2", name: "English Literature" },
    { code: "english3", name: "English Supplementary" },
    { code: "geo", name: "Human Geography" },
    { code: "geo2", name: "Practical Geography" },
    { code: "geo3", name: "Indian Geography" },
    { code: "history", name: "History" },
    { code: "home", name: "Home Science" },
    { code: "inf", name: "Informatics Practices" },
    { code: "math", name: "Mathematics" },
    { code: "pe", name: "Health and Physical Education" },
    { code: "phy", name: "Physics" },
    { code: "pol", name: "World Politics" },
    { code: "pol2", name: "Indian Politics" },
    { code: "psy", name: "Psychology" },
    { code: "soc", name: "Sociology" },
    { code: "soc2", name: "Social Change" }
  ]
};

export default function ChatPage() {
  const router = useRouter();
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [username, setUsername] = useState<string>('');
  const [selectedGrade, setSelectedGrade] = useState<string>("11");
  const [selectedSubjects, setSelectedSubjects] = useState<string[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentConversationId, setCurrentConversationId] = useState<string>('');
  const [isConversationsPanelOpen, setIsConversationsPanelOpen] = useState(true);
  const [shouldScrollToBottom, setShouldScrollToBottom] = useState(true);
  const [currentChat, setCurrentChat] = useState<string | null>(null);
  const [showOptionsFor, setShowOptionsFor] = useState<string | null>(null);
  const [editingConversation, setEditingConversation] = useState<string | null>(null);
  const [editedName, setEditedName] = useState('');

  const deleteConversation = async (id: string) => {
    try {
      await fetch(`http://localhost:5000/api/chats/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
  
      setConversations(prev => prev.filter(conv => {
        const convId = conv.conversation_id || conv._id;
        return convId !== id;
      }));
      
      if (currentConversationId === id || currentChat === id) {
        setCurrentChat(null);
        setCurrentConversationId('');
        setMessages([]);
      }
    } catch (error) {
      console.error('Error deleting conversation:', error);
    }
  };

  const loadUserChats = async () => {
    try {
      // console.log('Loading user chats...');
      const response = await fetch('http://localhost:5000/api/chats', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) throw new Error('Failed to load chats');
      
      const data = await response.json();
      if (data.success && data.conversations) {
        // Create conversations from chats
        const sortedConversations = data.conversations
          .sort((a: any, b: any) => 
            new Date(b.last_updated || b.timestamp).getTime() - 
            new Date(a.last_updated || a.timestamp).getTime());
        
        setConversations(sortedConversations);

        // If we currently have a selected conversation, find and update it in the list
        if (currentConversationId && !currentChat) {
          const current = sortedConversations.find(
            (conv: Conversation) => (conv.conversation_id || conv._id) === currentConversationId
          );
          if (current) {
            setCurrentChat(currentConversationId);
          }
        }
   
      }
      else{
        setConversations([]);
      }
      return true;
    } catch (error) {
      console.error('Error loading chats:', error);
      return false;
    }
  };
  
  const debugStreamData = (line: string) => {
    if (line.startsWith('data:')) {
      try {
        // console.log("Raw streaming data:", line);
        const jsonStr = line.slice(5).trim();
        const data = JSON.parse(jsonStr);
        // console.log("Parsed streaming data:", data);
        return data;
      } catch (error) {
        console.error("Failed to parse stream data:", error);
        console.error("Problematic string:", line.slice(5).trim());
        return null;
      }
    }
    return null;
  };

  const renameConversation = async (id: string, newName: string) => {
    try {
      const response = await fetch(`http://localhost:5000/api/chats/${id}/rename`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ name: newName })
      });

      if (!response.ok) throw new Error('Failed to rename conversation');

      setConversations(prev => prev.map(conv => {
        const convId = conv.conversation_id || conv._id;
        return (convId === id) ? { ...conv, name: newName } : conv;
      }));
      
      setEditingConversation(null);
      setEditedName('');
    } catch (error) {
      console.error('Error renaming conversation:', error);
    }
  };

  const loadConversationMessages = async (conversationId: string) => {
    try {
      const response = await fetch(`http://localhost:5000/api/chats/${conversationId}/messages`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
  
      if (!response.ok) throw new Error('Failed to load messages');
      
      const data = await response.json();
      
      if (data.success && data.messages) {
        const formattedMessages = data.messages.flatMap((msg: any) => [
          {
            id: `${msg.timestamp}-user`,
            sender: 'You',
            content: msg.user_input,
            timestamp: msg.timestamp
          },
          {
            id: `${msg.timestamp}-ai`,
            sender: 'AI',
            content: msg.bot_response,
            timestamp: msg.timestamp
          }
        ]);
        
        setMessages(formattedMessages);
      }
    } catch (error) {
      console.error('Error loading conversation messages:', error);
    }
  };

  const saveChat = async (userInput: string, botResponse: string, conversationId?: string) => {
    try {
      // console.log("Saving chat to conversation:", conversationId || currentConversationId);
      const response = await fetch('http://localhost:5000/api/chats', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          conversation_id: conversationId || currentConversationId,
          user_input: userInput,
          bot_response: botResponse,
          grade: selectedGrade,
          subjects: selectedSubjects
        })
      });
      
      const data = await response.json();
      if (data.success && data.conversation_id) {
        setCurrentConversationId(data.conversation_id);
        setCurrentChat(data.conversation_id);
      }
      
      // Refresh the chat history
      await loadUserChats();
    } catch (error) {
      console.error('Error saving chat:', error);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (currentConversationId) {
        loadUserChats();
    }
  }, [currentConversationId]);

  useEffect(() => {
    const abortController = new AbortController();
    
    return () => {
      abortController.abort();
      // Ensure loading is reset if component unmounts during loading
      if (loading) {
        setLoading(false);
      }
    };
  }, [loading]);

  useEffect(() => {
    console.log("Loading state changed:", loading);
  }, [loading]);

  useEffect(() => {
    console.log("Component mounted, loading user chats");
    loadUserChats().then(() => {
      console.log("Loaded conversations:", conversations);
    });
  }, []);

  useEffect(() => {
    if (shouldScrollToBottom) {
      scrollToBottom();
    }
  }, [messages, shouldScrollToBottom]);

  useEffect(() => {
    loadUserChats();
  }, []);

  useEffect(() => {
    if (currentConversationId) {
      loadConversationMessages(currentConversationId);
    }
  }, [currentConversationId]);
  
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
      return;
    }

    const fetchUser = async () => {
      try {
        const user = await authService.getUser();
        if (user) {
          setUsername(user.username);
          if (user.grade) {
            setSelectedGrade(user.grade);
          }
        } else {
          router.push('/login');
        }
      } catch (error) {
        console.error('Error fetching user data:', error);
        router.push('/login');
      }
    };

    fetchUser();
  }, [router]);

  const handleConversationClick = (conversation: Conversation) => {
    // Get conversation ID, supporting both formats
    const conversationId = conversation.conversation_id || conversation._id;
    
    setCurrentChat(conversationId);
    setCurrentConversationId(conversationId);
    
    // Handle loading messages
    if (conversation.messages && conversation.messages.length > 0) {
      // Messages are already in the conversation
      const formattedMessages = conversation.messages.flatMap(msg => [
        {
          id: `${msg.timestamp}-user`,
          sender: 'You',
          content: msg.user_input,
          timestamp: msg.timestamp
        },
        {
          id: `${msg.timestamp}-ai`,
          sender: 'AI',
          content: msg.bot_response,
          timestamp: msg.timestamp
        }
      ]);
      
      setMessages(formattedMessages);
    } 
    else {
      // Need to load messages from API
      loadConversationMessages(conversationId);
    }
    
    // Close conversations panel on mobile
    if (window.innerWidth < 768) {
      setIsConversationsPanelOpen(false);
    }
  };

  const fetchLatestResponse = async (conversationId: string, messageId: string) => {
    try {
      // console.log("Fetching final response from MongoDB for message:", messageId);
      const response = await fetch(`http://localhost:5000/api/chats/${conversationId}/messages`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      if (!response.ok) {
        throw new Error(`Failed to fetch response: ${response.status}`);
      }
      
      const data = await response.json();
      if (data.success && data.messages && data.messages.length > 0) {
        const latestMessage = data.messages[data.messages.length - 1];
        
        // console.log("MongoDB response retrieved:", 
        //   latestMessage.bot_response.substring(0, 50) + 
        //   (latestMessage.bot_response.length > 50 ? "..." : "")
        // );
        
        // Only update if we got a real response (not the placeholder)
        if (latestMessage.bot_response && 
            latestMessage.bot_response !== "AI is generating response..." &&
            latestMessage.bot_response !== "AI is typing...") {
          
          // console.log("Updating UI with MongoDB response for messageId:", messageId);

          setMessages(prev => {
            // First check if the message with this ID exists
            const messageExists = prev.some(msg => msg.id === messageId);
            
            if (messageExists) {
              // Update the existing message
              return prev.map(msg =>
                msg.id === messageId 
                  ? { ...msg, content: latestMessage.bot_response }
                  : msg
              );
            } else {
              // If message doesn't exist (rare case), create a complete set from MongoDB
              // console.log("Message ID not found, rebuilding from MongoDB");
              const formattedMessages = data.messages.flatMap((msg: any) => [
                {
                  id: `${msg.timestamp}-user`,
                  sender: 'You',
                  content: msg.user_input,
                  timestamp: msg.timestamp
                },
                {
                  id: `${msg.timestamp}-ai`,
                  sender: 'AI',
                  content: msg.bot_response,
                  timestamp: msg.timestamp
                }
              ]);
              return formattedMessages;
            }
          });
          
          // console.log("UI updated successfully");
          return true;
        } else {
          // console.log("MongoDB still has placeholder response, not updating UI");
        }
      }
      return false;
    } catch (error) {
      console.error("Error fetching response from MongoDB:", error);
      return false;
    }
  };

  const handleGradeChange = (grade: string) => {
    setSelectedGrade(grade);
    // Reset subjects when grade changes
    setSelectedSubjects([]);
  };

  const toggleSubject = (subject: string) => {
    setSelectedSubjects(prev => {
      if (prev.includes(subject)) {
        return prev.filter(s => s !== subject);
      } else {
        return [...prev, subject];
      }
    });
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newMessage.trim() || loading || selectedSubjects.length === 0) return;
  
    setLoading(true);
    const userInputText = newMessage;

    let receivedConversationId: string | null = null;
    let isNewConversation: boolean = false;
    
    try {
      // Create consistent message IDs
      const timestamp = new Date().toISOString();
      const messageTimestampBase = timestamp.replace(/[:.]/g, '-');
      
      // Add user message
      const userMessage = {
        id: `${messageTimestampBase}-user`,
        sender: 'You',
        content: userInputText,
        timestamp: timestamp
      };
  
      setMessages(prev => [...prev, userMessage]);
      setNewMessage('');
      inputRef.current?.focus();
  
      // Add initial AI message
      const aiMessageId = `${messageTimestampBase}-ai`;
      const aiMessage = {
        id: aiMessageId,
        sender: 'AI',
        content: '', 
        timestamp: timestamp
      };
      
      setMessages(prev => [...prev, aiMessage]);
  
      // Safety timeout
      const safetyTimeout = setTimeout(() => {
        // console.log("Safety timeout triggered");
        setLoading(false);
        setMessages(prev => 
          prev.map(msg => 
            msg.id === aiMessageId 
              ? { ...msg, content: "Response timeout. Please try again." }
              : msg
          )
        );
      }, 30000);
      
      // Get streaming response
      const response = await fetch('http://localhost:5000/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          conversation_id: currentConversationId || undefined,
          grade: selectedGrade,
          subjects: selectedSubjects,
          query: userInputText
        })
      });
      
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }
      
      const reader = response.body?.getReader();
      if (!reader) throw new Error('Response body cannot be read');
      
      const decoder = new TextDecoder();
      let receivedResponse = '';
      let streamComplete = false;
  
      // Cursor effect
      let blinkerVisible = true;
      const cursorBlinker = setInterval(() => {
        blinkerVisible = !blinkerVisible;
        setMessages(prev => 
          prev.map(msg => 
            msg.id === aiMessageId 
              ? { ...msg, content: receivedResponse + (blinkerVisible ? '' : '') }
              : msg
          )
        );
      }, 500);
      
      try {
        // Process the stream
        while (!streamComplete) {
          const { done, value } = await reader.read();
          
          if (done) {
            streamComplete = true;
            break;
          }
          
          const chunk = decoder.decode(value, { stream: true });
          const lines = chunk.split('\n');
          
          for (const line of lines) {
            if (line.trim().length === 0) continue;
            
            const data = debugStreamData(line);
            if (!data) continue;
            
            if (data.chunk) {
              const chars = data.chunk.split('');
              for (let i = 0; i < chars.length; i++) {
                receivedResponse += chars[i];
                
                if (i % 3 === 0 || i === chars.length - 1) {
                  setMessages(prev => 
                    prev.map(msg => 
                      msg.id === aiMessageId 
                        ? { ...msg, content: receivedResponse + '▋' }
                        : msg
                    )
                  );
                  
                  if (chars.length > 10) {
                    await new Promise(resolve => setTimeout(resolve, 10));
                  }
                }
              }
            }
            else if (data.done === true) {
              console.log("Stream complete");
              streamComplete = true;
              
              // If the backend created a new conversation, capture its ID
              if (data.conversation_id) {
                console.log("Received conversation ID:", data.conversation_id);
                receivedConversationId = data.conversation_id;
                isNewConversation = data.is_new_conversation === true;
                
                // Update current conversation immediately
                setCurrentConversationId(data.conversation_id);
                setCurrentChat(data.conversation_id);

                if (data.is_new_conversation) {
                  // Immediately add a placeholder conversation to the list
                  const newConversation: Conversation = {
                    _id: data.conversation_id,
                    name: format(new Date(), 'MMMM d, yyyy'),
                    timestamp: new Date().toISOString(),
                    messages: []
                  };
                  
                  setConversations(prev => [newConversation, ...prev]);
                  
                  // Still fetch from server to make sure we're in sync
                  setTimeout(() => loadUserChats(), 500);
                }
              }
            }
          }
        }
      } finally {
        clearInterval(cursorBlinker);
        clearTimeout(safetyTimeout);
        
        // Only save if we have a complete response
        if (receivedResponse.trim()) {
          // Update UI first
          setMessages(prev => 
            prev.map(msg => 
              msg.id === aiMessageId 
                ? { ...msg, content: receivedResponse }
                : msg
            )
          );
          
          // Save to MongoDB
          if (isNewConversation) {
            console.log("Using new conversation created by backend:", receivedConversationId);

            // if (receivedConversationId) {
            //   await loadConversationMessages(receivedConversationId);
            // }
            await new Promise(resolve => setTimeout(resolve, 300));
  
          // Force refresh of conversations list
          const success = await loadUserChats();
          if (!success) {
            // If first attempt fails, retry once more after a longer delay
            await new Promise(resolve => setTimeout(resolve, 700));
            await loadUserChats();
          }
            

            await loadUserChats();
            
          } else {
            // Only save to MongoDB if not a new conversation from backend
            try {
              const saveResponse = await fetch('http://localhost:5000/api/chats', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${localStorage.getItem('token')}`,
                  'Cache-Control': 'no-cache'
                },
                body: JSON.stringify({
                  conversation_id: receivedConversationId || currentConversationId || null,
                  user_input: userInputText,
                  bot_response: receivedResponse,
                  grade: selectedGrade,
                  subjects: selectedSubjects
                })
              });

              if (saveResponse.ok) {
                const saveData = await saveResponse.json();
                if (saveData.success && saveData.conversation_id) {
                  // Update the conversation ID
                  setCurrentConversationId(saveData.conversation_id);
                  setCurrentChat(saveData.conversation_id);
                  
                  // Reload messages to ensure UI and database are in sync
                  await loadConversationMessages(saveData.conversation_id);
                }
              }

              await loadUserChats();
              
      
              // Rest of your existing save code...
            } catch (error) {
              console.error('Failed to save chat:', error);
            }
          }
        }
      }
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => 
        prev.map(msg => 
          msg.id.endsWith('-ai') && msg.content === '▋'
            ? { ...msg, content: "An error occurred. Please try again." }
            : msg
        )
      );
    } finally {
      setLoading(false);
      await authService.updateActivity();
    }
  };

  const handleClearChat = async () => {
    setMessages([]);
    setNewMessage('');
    setCurrentConversationId('');
    setCurrentChat(null);
    
    // Focus input
    inputRef.current?.focus();
    
    // Close conversations panel on mobile
    if (window.innerWidth < 768) {
      setIsConversationsPanelOpen(false);
    }

    // Scroll to bottom of chat
    scrollToBottom();
  };

  const handleLogout = async () => {
    try {
      await authService.logout();
      router.push('/login');
    } catch (error) {
      console.error('Failed to logout:', error);
      // Show error message to user
      const errorMessage: Message = {
        id: Date.now().toString(),
        sender: 'System',
        content: 'Failed to logout properly. You will be redirected to login.',
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
      // Force redirect after showing error
      setTimeout(() => {
        router.push('/login');
      }, 2000);
    }
  };

  const formatTimestamp = (timestamp: string) => {
    try {
      return format(new Date(timestamp), 'h:mm a');
    } catch {
      return '';
    }
  };

  const closeSidebar = () => {
    setIsSidebarOpen(false);
  };

  return (
    <div className="flex h-screen w-full bg-gray-50 dark:bg-gray-900">
      {/* Mobile overlay */}
      {isSidebarOpen && (
        <div 
          className="fixed inset-0 z-10 bg-black/50 md:hidden" 
          onClick={closeSidebar}
          aria-hidden="true"
        />
      )}

      {/* Mobile menu button */}
      <button
        onClick={() => setIsSidebarOpen(!isSidebarOpen)}
        className="fixed left-4 top-4 z-30 rounded-full bg-gray-700 p-2 text-white shadow-lg md:hidden"
        aria-label="Toggle menu"
      >
        {isSidebarOpen ? <FiX className="size-5" /> : <FiMenu className="size-5" />}
      </button>

      {/* Sidebar */}
      <div className={`fixed inset-y-0 z-20 w-72 bg-gray-900 shadow-xl transition-transform duration-300 ease-in-out md:relative md:translate-x-0 ${
        isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
      }`}>
        <div className="flex h-full flex-col">
          {/* App Title */}
          <div className="border-b border-gray-700 p-6">  
            <h1 className="text-xl font-bold text-white">OliveOrange AI</h1>
            <p className="mt-1 text-sm text-gray-400">Your Study Assistant</p>
          </div>

          {/* Grade Selection */}
          <div className="border-b border-gray-700 p-4">
            <h2 className="mb-2 text-sm font-medium text-gray-400">Select Grade</h2>
            <div className="flex flex-wrap gap-2">
              {GRADES.map((grade) => (
                <button
                  key={grade}
                  onClick={() => handleGradeChange(grade)}
                  className={`rounded-full px-4 py-2 text-sm font-medium transition-colors ${
                    selectedGrade === grade
                      ? 'bg-indigo-600 text-white'
                      : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                  }`}
                >
                  Grade {grade}
                </button>
              ))}
            </div>
          </div>

          {/* Subject Selection */}
          <div className="flex-1 overflow-y-auto border-b border-gray-700">
            <div className="p-4">
              <h2 className="mb-2 text-sm font-medium text-gray-400">Select Subjects</h2>
              <div className="space-y-2">
                {SUBJECTS[selectedGrade as keyof typeof SUBJECTS].map((subject) => (
                  <button
                    key={subject.code}
                    onClick={() => toggleSubject(subject.code)}
                    className={`flex w-full items-center justify-between rounded-lg px-4 py-2 text-sm font-medium transition-colors ${
                      selectedSubjects.includes(subject.code)
                        ? 'bg-indigo-600 text-white'
                        : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                    }`}
                  >
                    <div className="flex flex-col items-start">
                      <span className="font-medium">{subject.name}</span>
                      <span className="text-xs opacity-75">{subject.code}</span>
                    </div>
                    {selectedSubjects.includes(subject.code) && (
                      <FiCheck className="size-4" />
                    )}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="border-t border-gray-700 p-4">
            <button
              onClick={handleClearChat}
              className="mb-4 w-full rounded-md border border-gray-700 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-gray-700"
              aria-label="Clear conversation"
            >
              Clear conversation
            </button>
          </div>

          {/* User Section */}
          <div className="border-t border-gray-700 p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="flex size-9 items-center justify-center rounded-full bg-indigo-600">
                  <FiUser className="size-5 text-white" />
                </div>
                <span className="font-medium text-white">{username || 'Loading...'}</span>
              </div>
              <div className="flex items-center gap-2">
                <a
                  href="/profile"
                  className="rounded-md p-2 text-gray-400 hover:bg-gray-700"
                  aria-label="Profile settings"
                >
                  <FiSettings className="size-5" />
                </a>
                <button
                  onClick={handleLogout}
                  className="rounded-md p-2 text-gray-400 hover:bg-gray-700"
                  aria-label="Logout"
                >
                  <FiLogOut className="size-5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex flex-1 flex-col overflow-hidden">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-4 py-6 md:px-6">
          <div className="mx-auto max-w-3xl">
            {messages.length === 0 ? (
              <div className="flex h-full flex-col items-center justify-center p-8 text-center">
                <div className="mb-6 rounded-full bg-indigo-100 p-6 dark:bg-gray-800">
                  <FiMessageSquare className="size-12 text-indigo-600 dark:text-indigo-400" />
                </div>
                <h1 className="mb-3 text-4xl font-bold text-gray-900 dark:text-white">
                  OliveOrange AI Assistant
                </h1>
                <p className="max-w-md text-lg text-gray-600 dark:text-gray-400">
                  Start a conversation and get help with your studies! Ask questions about any subject to get started.
                </p>
              </div>
            ) : (
              <div className="space-y-6">
                <div className="border-b border-gray-200 pb-4 text-center dark:border-gray-700">
                  <span className="text-sm text-gray-500">
                    Beginning of conversation
                  </span>
                </div>
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex items-start ${
                      message.sender === 'You' ? 'justify-end' : 'justify-start'
                    }`}
                  >
                    {message.sender !== 'You' && (
                      <div className="mr-3 flex size-10 shrink-0 items-center justify-center rounded-full bg-indigo-600">
                        <FiUser className="size-5 text-white" />
                      </div>
                    )}
                    <div className="flex flex-col">
                      <div
                        className={`max-w-md rounded-2xl px-4 py-3 ${
                          message.sender === 'You'
                            ? 'bg-indigo-600 text-white'
                            : 'bg-white shadow dark:bg-gray-800 dark:text-white'
                        }`}
                      >
                        {/* Render AI message content with formatting */}
                        {message.sender === 'AI' ? (
                          <ReactMarkdown
                            remarkPlugins={[remarkGfm]}
                            components={{
                              h1: ({ node, ...props }) => <h1 className="text-2xl font-bold" {...props} />,
                              h2: ({ node, ...props }) => <h2 className="text-xl font-semibold" {...props} />,
                              p: ({ node, ...props }) => <p className="text-base leading-relaxed" {...props} />,
                              ul: ({ node, ...props }) => <ul className="ml-5 list-disc" {...props} />,
                              ol: ({ node, ...props }) => <ol className="ml-5 list-decimal" {...props} />,
                              li: ({ node, ...props }) => (
                                <ul>
                                  <li className="mb-1" {...props} />
                                </ul>
                              ),
                              strong: ({ node, ...props }) => <strong className="font-bold" {...props} />,
                              em: ({ node, ...props }) => <em className="italic" {...props} />,
                              a: ({ node, href, children, ...props }) => {
                                if (href && href.includes('/test')) {
                                  return (
                                    <button
                                      onClick={() => window.location.href = href}
                                      className="inline-flex items-center rounded-md bg-indigo-600 px-3 py-1 text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                                    >
                                      Go To Test
                                    </button>
                                  );
                                }
                                return (
                                  <a 
                                    href={href}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-blue-600 underline hover:text-blue-800"
                                    {...props}
                                  >
                                    {children}
                                  </a>
                                );
                              },
                            }}
                          >
                            {message.content}
                          </ReactMarkdown>
                        ) : (
                          <div className="whitespace-pre-wrap">{message.content}</div>
                        )}
                      </div>
                      <span className={`mt-1 text-xs ${message.sender === 'You' ? 'self-end' : ''} text-gray-500`}>
                        {formatTimestamp(message.timestamp)}
                      </span>
                    </div>
                    {message.sender === 'You' && (
                      <div className="ml-3 flex size-10 shrink-0 items-center justify-center rounded-full bg-gray-700">
                        <FiUser className="size-5 text-white" />
                      </div>
                    )}
                  </div>
                ))}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>
        </div>

        {/* Message Input */}
        <div className="border-t border-gray-200 bg-white p-4 md:p-6 dark:border-gray-700 dark:bg-gray-800">
          <form onSubmit={handleSendMessage} className="mx-auto max-w-3xl">
            <div className="relative flex items-center">
              <input
                ref={inputRef}
                type="text"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                placeholder={selectedSubjects.length === 0 ? "Please select at least one subject..." : "Type your message..."}
                className="w-full rounded-full border border-gray-300 bg-white px-6 py-3 pr-16 text-gray-900 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                disabled={loading || selectedSubjects.length === 0}
              />
              <button
                type="submit"
                disabled={loading || !newMessage.trim() || selectedSubjects.length === 0}
                className={`absolute right-2 rounded-full p-2 ${
                  loading || !newMessage.trim() || selectedSubjects.length === 0
                    ? 'text-gray-400' 
                    : 'bg-indigo-600 text-white hover:bg-indigo-700'
                } transition-all`}
                aria-label="Send message"
              >
                <FiSend className="size-5" />
              </button>
            </div>
            {loading && (
              <div className="mt-2 text-center text-sm text-gray-500">
                AI is typing...
              </div>
            )}
            {selectedSubjects.length === 0 && (
              <div className="mt-2 text-center text-sm text-red-500">
                Please select at least one subject to continue
              </div>
            )}
          </form>
        </div>
      </div>
      
      {/* Conversations Panel */}
      <div 
        className={`fixed right-0 top-0 z-20 h-full transform bg-gray-800 transition-transform duration-300 ease-in-out ${
          isConversationsPanelOpen ? 'translate-x-0' : 'translate-x-full'
        }`}
        style={{ width: '300px' }}
      >
        <div className="border-b border-gray-700 p-4">
          <h2 className="text-lg font-semibold text-white">Chat History</h2>
          {/* Add New Chat button */}
          <button
            onClick={handleClearChat}
            className="mt-2 w-full rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-indigo-700"
          >
            New Chat
          </button>

          <button
            onClick={() => window.location.href = '/tests'}
            className="mt-2 w-full rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-indigo-700"
          >
            Go to Tests
          </button>
        </div>
        
        {/* Arrow button for expand/collapse */}
        <button
          onClick={() => setIsConversationsPanelOpen(!isConversationsPanelOpen)}
          className="absolute -left-10 top-1/2 transform rounded-l-lg bg-gray-800 p-2 text-white"
          aria-label={isConversationsPanelOpen ? "Collapse sidebar" : "Expand sidebar"}
        >
          {isConversationsPanelOpen ? 
            <FiChevronRight className="size-6" /> : 
            <FiChevronLeft className="size-6" />
          }
        </button>

        <div className="flex h-full flex-col">
          <div className="flex-1 overflow-y-auto">
            {conversations.map((conversation) => {
              const convId = conversation.conversation_id || conversation._id;
              return (
                <div
                  key={convId}
                  className={`cursor-pointer border-b border-gray-700 p-4 hover:bg-gray-700 ${
                    currentChat === convId ? 'bg-gray-700' : ''
                  }`}
                  onClick={() => handleConversationClick(conversation)}
                  onMouseEnter={() => setShowOptionsFor(convId)}
                  onMouseLeave={() => setShowOptionsFor(null)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      {editingConversation === convId ? (
                        <input
                          type="text"
                          value={editedName}
                          onChange={(e) => setEditedName(e.target.value)}
                          onKeyDown={(e) => {
                            if (e.key === 'Enter') {
                              e.preventDefault();
                              renameConversation(convId, editedName);
                              setEditingConversation(null);
                            } else if (e.key === 'Escape') {
                              setEditingConversation(null);
                            }
                          }}
                          onBlur={() => {
                            if (editedName.trim()) {
                              renameConversation(convId, editedName);
                            }
                            setEditingConversation(null);
                          }}
                          className="w-full bg-gray-600 px-2 py-1 text-sm text-white focus:outline-none focus:ring-1 focus:ring-indigo-500"
                          autoFocus
                          onClick={(e) => e.stopPropagation()}
                        />
                      ) : (
                        <div className="flex items-center gap-2">
                          <h3 className="text-sm font-medium text-white">
                            {conversation.name}
                          </h3>
                          {showOptionsFor === convId && (
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                setEditingConversation(convId);
                                setEditedName(conversation.name);
                              }}
                              className="rounded p-1 text-gray-400 hover:bg-gray-600"
                            >
                              <FiEdit2 className="size-3" />
                            </button>
                          )}
                        </div>
                      )}
                      <p className="mt-1 text-xs text-gray-400">
                        {format(new Date(conversation.timestamp || conversation.last_updated || conversation.created_at|| new Date()), 'h:mm a')}
                      </p>
                    </div>
                    
                    {showOptionsFor === convId && !editingConversation && (
                      <div className="flex items-center gap-2">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            if (confirm('Are you sure you want to delete this chat?')) {
                              deleteConversation(convId);
                            }
                          }}
                          className="rounded p-2 text-gray-400 hover:bg-gray-600"
                        >
                          <FiTrash2 className="size-4" />
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
            {conversations.length === 0 && (
              <div className="p-4 text-center text-sm text-gray-400">
                No chat history yet
              </div>
            )}
          </div>
        </div>
      </div>
      

      <button
        onClick={() => setIsConversationsPanelOpen(!isConversationsPanelOpen)}
        className="fixed right-4 top-4 z-30 rounded-full bg-gray-700 p-2 text-white shadow-lg md:hidden"
      >
        <FiMessageSquare className="size-5" />
      </button>
    </div>
  );
}