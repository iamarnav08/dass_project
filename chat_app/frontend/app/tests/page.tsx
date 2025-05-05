'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Button, Card, Label, TextInput, Modal, Select, Spinner, Badge } from 'flowbite-react';
import { FiPlus, FiArrowLeft, FiCheckCircle, FiXCircle, FiClipboard, FiCheck } from 'react-icons/fi';
import { authService } from '@/lib/auth';
// API base URL
const API_URL = 'http://localhost:5000';

// Copy subject data from chat page to have consistent options
const SUBJECTS = {
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

interface Test {
  _id: string;
  title: string;
  topic: string;
  grade: string;
  subjects: string[];
  created_at: string;
  attempts?: number;
  best_score?: number;
  last_attempt_score?: number;
  last_attempt_date?: string;
  attempt_history?: { attempt_id: string; score: number; timestamp: string }[];
}

interface Question {
  id: number;
  text: string;
  options: string[];
  correctAnswer?: string;
}

export default function TestsPage() {
  const router = useRouter();
  const [tests, setTests] = useState<Test[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showNewTestModal, setShowNewTestModal] = useState(false);
  const [currentTest, setCurrentTest] = useState<any>(null);
  const [userAnswers, setUserAnswers] = useState<Record<number, string>>({});
  const [testResults, setTestResults] = useState<any>(null);
  const [selectedOption, setSelectedOption] = useState<Record<number, number>>({});
  const [confirmDelete, setConfirmDelete] = useState<string | null>(null);

  // New test form state
  const [newTestData, setNewTestData] = useState<{
    title: string;
    topic: string;
    grade: string;
    subjects: string[];
    num_questions: number;
  }>({
    title: '',
    topic: '',
    grade: '10',
    subjects: [],
    num_questions: 5
  });

  // Helper function to get auth token
  const getAuthToken = () => localStorage.getItem('token');

  // Helper for API requests
  const fetchAPI = async (endpoint: string, options = {}) => {
    try {
      const token = getAuthToken();
      const defaultOptions = {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : '',
        },
      };
      
      const response = await fetch(`${API_URL}${endpoint}`, {
        ...defaultOptions,
        ...options,
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.message || `API error: ${response.status}`);
      }
      
      return data;
    } catch (error) {
      console.error(`API request failed: ${error}`);
      throw error;
    }
  };

  const loadTests = async () => {
    try {
      setLoading(true);
      const response = await fetchAPI('/api/tests');
      if (response.success) {
        setTests(response.tests || []);
      } else {
        console.error('Failed to load tests:', response.message);
        // Don't show error to user, just log it
      }
    } catch (err) {
      console.error('Error loading tests:', err);
      // Don't show error to user, just log it
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTests();
  }, []);

  const handleCreateTest = async () => {
    try {
      setLoading(true);
      // Validate required fields
      if (!newTestData.title.trim() || !newTestData.topic.trim() || newTestData.subjects.length === 0) {
        setError('Please fill in all required fields and select at least one subject');
        setLoading(false);
        return;
      }
      
      // Map subject codes to subject names for the API
      const subjectNames = newTestData.subjects.map(code => {
        // Find the subject name corresponding to the code
        const subjectObj = SUBJECTS[newTestData.grade as "10" | "11" | "12"]?.find(s => s.code === code);
        return subjectObj ? subjectObj.name : code;
      });
      
      const response = await fetchAPI('/api/generate_test', {
        method: 'POST',
        body: JSON.stringify({
          ...newTestData,
          subjects: subjectNames // Send names instead of codes to the API
        }),
      });
      
      if (response.success) {
        setShowNewTestModal(false);
        await loadTests();
        // Show the newly created test
        router.push(`/tests/${response.test_id}`);  
      } else {
        setError(response.message || 'Failed to create test');
      }
    } catch (err: any) {
      setError(err.message || 'Error creating test. Please try again.');
      console.error('Error creating test:', err);
    } finally {
      setLoading(false);
      await authService.updateActivity();
    }
  };

  const handleStartTest = async (testId: string) => {
    try {
      // Format the test ID to ensure it's valid
      const formattedTestId = String(testId).trim();
      
      // Validate test ID before navigation
      if (!formattedTestId || formattedTestId === 'undefined' || formattedTestId === 'null') {
        console.error('Invalid test ID detected:', formattedTestId);
        setError('Invalid test ID. Please reload the page and try again.');
        return;
      }
      
      // Log the ID we're using (helpful for debugging)
      console.log(`Navigating to test: ${formattedTestId}`);
      
      // Navigate to the test slug page
      router.push(`/tests/${formattedTestId}`);
    } catch (err) {
      setError('Error starting test. Please try again.');
      console.error('Error starting test:', err);
    }
  };

  const handleDeleteTest = async (testId: string) => {
    try {
      setLoading(true);
      await fetchAPI(`/api/tests/${testId}`, {
        method: 'DELETE'
      });
      
      // Remove the deleted test from the list
      setTests(prevTests => prevTests.filter(test => test._id !== testId));
      setConfirmDelete(null);
      
    } catch (err: any) {
      setError(err.message || 'Error deleting test. Please try again.');
      console.error('Error deleting test:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectAnswer = (questionId: number, optionIndex: number) => {
    setSelectedOption({
      ...selectedOption,
      [questionId]: optionIndex
    });
    setUserAnswers({
      ...userAnswers,
      [questionId]: currentTest.questions[questionId].options[optionIndex]
    });
  };

  const handleSubmitTest = async () => {
    try {
      setLoading(true);
      // Convert answers to required format
      const formattedAnswers = Object.keys(userAnswers).map(questionId => ({
        question_id: parseInt(questionId),
        answer: userAnswers[parseInt(questionId)]
      }));

      const response = await fetchAPI('/api/evaluate_test', {
        method: 'POST',
        body: JSON.stringify({
          test_id: currentTest._id,
          answers: formattedAnswers
        }),
      });

      if (response.success) {
        setTestResults(response);
      } else {
        setError(response.message || 'Failed to evaluate test');
      }
    } catch (err) {
      setError('Error evaluating test. Please try again.');
      console.error('Error evaluating test:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleBackToTests = () => {
    setCurrentTest(null);
    setTestResults(null);
    loadTests();
  };

  const handleGradeChange = (grade: string) => {
    setNewTestData({
      ...newTestData,
      grade: grade,
      subjects: [] // Reset subjects when grade changes
    });
  };

  const toggleSubject = (subjectCode: string) => {
    setNewTestData(prev => {
      const subjects = [...prev.subjects];
      const index = subjects.indexOf(subjectCode);
      
      if (index >= 0) {
        subjects.splice(index, 1); // Remove the subject
      } else {
        subjects.push(subjectCode); // Add the subject
      }
      
      return {
        ...prev,
        subjects
      };
    });
  };

  // Render test list with enhanced UI
  const renderTestList = () => (
    <div className="container mx-auto p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">My Tests</h1>
        <Button 
          onClick={() => setShowNewTestModal(true)} 
          color="blue"
          className="bg-indigo-600 hover:bg-indigo-700 focus:ring-indigo-500"
        >
          <FiPlus className="mr-2" /> New Test
        </Button>
      </div>

      {loading ? (
        <div className="flex justify-center my-8">
          <Spinner size="xl" />
        </div>
      ) : tests.length === 0 ? (
        <div className="text-center p-8 bg-white dark:bg-gray-800 rounded-lg shadow-md">
          <div className="mb-6 rounded-full bg-indigo-100 p-6 dark:bg-gray-700 mx-auto w-24">
            <FiClipboard className="size-12 text-indigo-600 dark:text-indigo-400 mx-auto" />
          </div>
          <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-2">No Tests Found</h2>
          <p className="text-gray-600 dark:text-gray-400 mb-6">Create your first test to practice and assess your knowledge.</p>
          <Button 
            color="blue"
            className="bg-indigo-600 hover:bg-indigo-700 focus:ring-indigo-500"
            onClick={() => setShowNewTestModal(true)}
          >
            <FiPlus className="mr-2" /> Create Your First Test
          </Button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {tests.map((test) => (
            <Card key={test._id} className="hover:shadow-lg transition-shadow">
              <h5 className="text-xl font-bold tracking-tight text-gray-900 dark:text-white">
                {test.title}
              </h5>
              <div className="flex gap-2 mb-3 flex-wrap">
                <Badge color="info">{test.grade}</Badge>
                {test.subjects.map((subject, index) => (
                  <Badge key={index} color="dark">{subject}</Badge>
                ))}
              </div>
              <p className="font-normal text-gray-700 dark:text-gray-400 mb-4">
                Topic: {test.topic}
              </p>
              
              {/* Simplified test statistics display focusing on highest score */}
              <div className="bg-gray-50 dark:bg-gray-700 rounded p-3 mb-4">
                {test.best_score !== undefined && (
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium text-gray-600 dark:text-gray-400">
                      Highest Score:
                    </span>
                    <span className={`text-2xl font-bold ${
                      test.best_score >= 70 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'
                    }`}>
                      {test.best_score}%
                    </span>
                  </div>
                )}
                
                {/* Previous scores section */}
                {test.attempt_history && test.attempt_history.length > 0 && (
                  <div className="mt-3 pt-2 border-t border-gray-200 dark:border-gray-600">
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">Previous Scores:</p>
                    <div className="flex flex-wrap gap-1">
                      {test.attempt_history.map((attempt, index) => (
                        <span 
                          key={attempt.attempt_id} 
                          className={`text-xs px-2 py-1 rounded-full ${
                            attempt.score >= 70 
                              ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300' 
                              : 'bg-gray-100 text-gray-800 dark:bg-gray-600 dark:text-gray-300'
                          }`}
                          title={`${new Date(attempt.timestamp).toLocaleString()}`}
                        >
                          {attempt.score}%
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                
                {test.last_attempt_date && (
                  <div className="text-xs text-gray-500 dark:text-gray-400 mt-2 text-right">
                    Last attempt: {new Date(test.last_attempt_date).toLocaleDateString()}
                  </div>
                )}
              </div>
              
              <div className="flex gap-2">
                <Button 
                  onClick={() => {
                    // Extract the ID value, handling different possible formats
                    const testId = test._id;
                    
                    if (testId && typeof testId === 'string') {
                      handleStartTest(testId);
                    } else if (testId) {
                      // If it's not a string but exists, convert it to string
                      handleStartTest(String(testId));
                    } else {
                      setError(`Cannot start test: Invalid or missing ID`);
                      console.error('Invalid test ID format:', test);
                    }
                  }} 
                  color="blue" 
                  className="flex-1"
                >
                  {test.attempts && test.attempts > 0 ? 'Retake Test' : 'Start Test'}
                </Button>
                <Button 
                  onClick={() => setConfirmDelete(test._id)} 
                  color="failure"
                >
                  Delete
                </Button>
              </div>
            </Card>
          ))}
        </div>
      )}

      <Button 
        color="light" 
        className="mt-6 dark:bg-gray-700 dark:text-white dark:hover:bg-gray-600"
        onClick={() => router.push('/chat')}
      >
        <FiArrowLeft className="mr-2" /> Back to Chat
      </Button>
    </div>
  );

  // Render test taking interface
  const renderTestInterface = () => {
    if (!currentTest) return null;

    return (
      <div className="container mx-auto p-4">
        <Button className="mb-4" onClick={handleBackToTests}>
          <FiArrowLeft className="mr-2" /> Back to Tests
        </Button>

        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-md">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">{currentTest.title}</h1>
          <p className="text-gray-600 dark:text-gray-400 mb-6">Topic: {currentTest.topic}</p>

          {currentTest.questions.map((question: Question, qIndex: number) => (
            <div key={qIndex} className="mb-6 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg shadow-sm">
              <p className="font-medium mb-3 text-gray-900 dark:text-white">
                {qIndex + 1}. {question.text}
              </p>
              <div className="space-y-2">
                {question.options.map((option: string, oIndex: number) => (
                  <div key={oIndex} className="flex items-center p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors">
                    <input
                      type="radio"
                      id={`q${qIndex}-o${oIndex}`}
                      name={`question-${qIndex}`}
                      className="w-4 h-4 text-blue-600"
                      checked={selectedOption[qIndex] === oIndex}
                      onChange={() => handleSelectAnswer(qIndex, oIndex)}
                    />
                    <label
                      htmlFor={`q${qIndex}-o${oIndex}`}
                      className="ml-2 w-full text-gray-700 dark:text-gray-300 cursor-pointer"
                    >
                      {option}
                    </label>
                  </div>
                ))}
              </div>
            </div>
          ))}

          <Button
            color="blue"
            onClick={handleSubmitTest}
            disabled={Object.keys(userAnswers).length !== currentTest.questions.length}
            className="w-full md:w-auto"
          >
            Submit Test
          </Button>
        </div>
      </div>
    );
  };

  // Render test results with enhanced UI
  const renderTestResults = () => {
    if (!testResults || !currentTest) return null;

    return (
      <div className="container mx-auto p-4">
        <Button color="light" className="mb-4" onClick={handleBackToTests}>
          <FiArrowLeft className="mr-2" /> Back to Tests
        </Button>

        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-md">
          <div className="text-center mb-6">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Test Results</h1>
            <h2 className="text-xl text-gray-700 dark:text-gray-300">{testResults.test_title}</h2>
            <div className="mt-4 text-3xl font-bold">
              <span className={testResults.score >= 70 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}>
                Score: {testResults.score}%
              </span>
            </div>
          </div>

          <div className="space-y-6">
            {testResults.evaluation.map((result: any, index: number) => (
              <div key={index} className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg shadow-sm">
                <div className="flex items-center mb-2">
                  {result.is_correct ? (
                    <FiCheckCircle className="text-green-500 mr-2 text-xl flex-shrink-0" />
                  ) : (
                    <FiXCircle className="text-red-500 mr-2 text-xl flex-shrink-0" />
                  )}
                  <p className="font-medium text-gray-900 dark:text-white">
                    Question {index + 1}: {currentTest.questions[index].text}
                  </p>
                </div>
                <div className="ml-7">
                  <p className={`text-sm ${result.is_correct ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'} mb-1`}>
                    Your answer: {result.user_answer}
                  </p>
                  <p className="text-sm text-green-600 dark:text-green-400 mb-2">
                    Correct answer: {result.correct_answer}
                  </p>
                  {result.explanation && (
                    <div className="mt-2 text-sm bg-blue-50 dark:bg-blue-900 p-3 rounded">
                      <p className="font-medium text-blue-800 dark:text-blue-200">Explanation:</p>
                      <p className="text-blue-700 dark:text-blue-300">{result.explanation}</p>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
          
          <Button 
            color="blue" 
            onClick={handleBackToTests} 
            className="w-full md:w-auto mt-6"
          >
            Back to Tests
          </Button>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900">
      {error && (
        <div className="p-4 bg-red-100 text-red-700 rounded-md mx-4 mt-4">
          {error}
          <button className="ml-4 font-bold" onClick={() => setError(null)}>
            Dismiss
          </button>
        </div>
      )}

      {testResults ? renderTestResults() : currentTest ? renderTestInterface() : renderTestList()}

      {/* Enhanced modal with improved UI for test creation */}
      <Modal 
        show={showNewTestModal} 
        onClose={() => setShowNewTestModal(false)}
        size="xl"
        popup
        className="dark:bg-gray-800"
      >
        <Modal.Header className="border-b border-gray-200 dark:border-gray-700 dark:bg-gray-800 dark:text-white">
          Create New Test
        </Modal.Header>
        <Modal.Body className="dark:bg-gray-800 overflow-y-auto max-h-[80vh]">
          <div className="space-y-4">
            <div>
              <Label htmlFor="title" className="text-sm font-medium dark:text-gray-300">Test Title</Label>
              <TextInput
                id="title"
                placeholder="Enter test title"
                value={newTestData.title}
                onChange={(e) => setNewTestData({ ...newTestData, title: e.target.value })}
                required
                className="mt-1 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              />
            </div>
            <div>
              <Label htmlFor="topic" className="text-sm font-medium dark:text-gray-300">Topic</Label>
              <TextInput
                id="topic"
                placeholder="e.g. Photosynthesis, Quadratic Equations"
                value={newTestData.topic}
                onChange={(e) => setNewTestData({ ...newTestData, topic: e.target.value })}
                required
                className="mt-1 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              />
            </div>
            
            <div>
              <Label htmlFor="grade" className="text-sm font-medium dark:text-gray-300">Grade</Label>
              <div className="flex flex-wrap gap-2 mt-2">
                {["10", "11", "12"].map((grade) => (
                  <button
                    key={grade}
                    type="button"
                    onClick={() => handleGradeChange(grade)}
                    className={`rounded-full px-4 py-2 text-sm font-medium transition-colors ${
                      newTestData.grade === grade
                        ? 'bg-indigo-600 text-white'
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
                    }`}
                  >
                    Grade {grade}
                  </button>
                ))}
              </div>
            </div>
            
            <div className="mb-4">
              <Label className="text-sm font-medium dark:text-gray-300 mb-2 block">
                Select Subjects (choose at least one)
              </Label>
              <div className="max-h-[200px] overflow-y-auto p-1 border border-gray-300 dark:border-gray-600 rounded">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {SUBJECTS[newTestData.grade as keyof typeof SUBJECTS].map(subject => (
                    <div 
                      key={subject.code}
                      onClick={() => toggleSubject(subject.code)}
                      className={`flex items-center justify-between px-3 py-2 rounded-lg cursor-pointer ${
                        newTestData.subjects.includes(subject.code)
                          ? 'bg-indigo-600 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
                      }`}
                    >
                      <div>
                        <p className="font-medium">{subject.name}</p>
                        <p className="text-xs opacity-75">{subject.code}</p>
                      </div>
                      {newTestData.subjects.includes(subject.code) && (
                        <FiCheck className="size-5" />
                      )}
                    </div>
                  ))}
                </div>
              </div>
              {newTestData.subjects.length === 0 && (
                <p className="mt-1 text-xs text-red-500">Please select at least one subject</p>
              )}
            </div>

            <div>
              <Label htmlFor="numQuestions" className="text-sm font-medium dark:text-gray-300">Number of Questions</Label>
              <div className="flex flex-wrap gap-2 mt-2">
                {[3, 5, 10, 15].map((num) => (
                  <button
                    key={num}
                    type="button"
                    onClick={() => setNewTestData({ ...newTestData, num_questions: num })}
                    className={`rounded-full px-4 py-2 text-sm font-medium transition-colors ${
                      newTestData.num_questions === num
                        ? 'bg-indigo-600 text-white'
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
                    }`}
                  >
                    {num} Questions
                  </button>
                ))}
              </div>
            </div>
          </div>
        </Modal.Body>
        <Modal.Footer className="dark:bg-gray-800 dark:border-gray-700 flex justify-end gap-2">
          <Button 
            color="blue" 
            onClick={handleCreateTest} 
            disabled={loading || newTestData.subjects.length === 0} 
            className="w-full sm:w-auto bg-indigo-600 hover:bg-indigo-700 focus:ring-indigo-500"
          >
            {loading ? <Spinner size="sm" className="mr-2" /> : <FiPlus className="mr-2" />}
            Create Test
          </Button>
          <Button 
            onClick={() => setShowNewTestModal(false)} 
            className="w-full sm:w-auto dark:bg-gray-700 dark:text-white dark:hover:bg-gray-600"
          >
            Cancel
          </Button>
        </Modal.Footer>
      </Modal>

      {/* Delete confirmation dialog */}
      <Modal
        show={!!confirmDelete}
        size="md"
        popup
        onClose={() => setConfirmDelete(null)}
      >
        <Modal.Header />
        <Modal.Body>
          <div className="text-center">
            <h3 className="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400">
              Are you sure you want to delete this test?
            </h3>
            <div className="flex justify-center gap-4">
              <Button
                color="failure"
                onClick={() => confirmDelete && handleDeleteTest(confirmDelete)}
              >
                Yes, delete it
              </Button>
              <Button
                color="gray"
                onClick={() => setConfirmDelete(null)}
              >
                Cancel
              </Button>
            </div>
          </div>
        </Modal.Body>
      </Modal>
    </div>
  );
}
