'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Button, Spinner, Badge } from 'flowbite-react';
import { FiArrowLeft, FiCheckCircle, FiXCircle, FiBarChart2 } from 'react-icons/fi';

const API_URL = 'http://localhost:5000';

interface Question {
  id: number;
  text: string;
  options: string[] | { letter: string, text: string }[];
  correctAnswer?: string;
}

interface AttemptHistory {
  score: number;
  timestamp: string;
  attempt_id: string;
}

export default function TestPage() {
  const params = useParams();
  const router = useRouter();
  const [currentTest, setCurrentTest] = useState<any>(null);
  const [userAnswers, setUserAnswers] = useState<Record<number, string>>({});
  const [testResults, setTestResults] = useState<any>(null);
  const [selectedOption, setSelectedOption] = useState<Record<number, number>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [attemptHistory, setAttemptHistory] = useState<AttemptHistory[]>([]);

  const testId = params?.id as string;

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

  const loadTest = async () => {
    try {
      setLoading(true);

      // Get testId from params and ensure it's properly formatted
      const formattedTestId = String(testId).trim();

      // Validate test ID before making API call
      if (!formattedTestId || formattedTestId === 'undefined' || formattedTestId === 'null') {
        console.error('Invalid test ID detected:', formattedTestId);
        setError('Invalid test ID. Please return to the tests page and try again.');
        setLoading(false);
        return;
      }

      console.log(`Loading test with ID: ${formattedTestId}`);

      const response = await fetchAPI(`/api/tests/${formattedTestId}`);

      if (response.success) {
        console.log('Test loaded successfully');
        setCurrentTest(response.test);
        setUserAnswers({});
        setSelectedOption({});
        setTestResults(null);
      } else {
        setError(response.message || 'Failed to load test');
      }
    } catch (err: any) {
      const errorMessage = err.message || 'Error loading test. Please try again.';
      setError(errorMessage);
      console.error('Error loading test:', err);
    } finally {
      setLoading(false);
    }
  };

  // Call loadTest when testId changes, with validation
  useEffect(() => {
    console.log('Test ID from URL params:', testId, typeof testId);

    // Ensure we have a valid test ID
    const formattedTestId = String(testId).trim();

    if (formattedTestId && formattedTestId !== 'undefined' && formattedTestId !== 'null') {
      loadTest();
    } else {
      setError('Invalid or missing test ID');
      setLoading(false);
    }
  }, [testId]);

  // Helper function to get option text regardless of format
  const getOptionText = (option: any): string => {
    if (typeof option === 'string') {
      return option;
    } else if (option && typeof option === 'object' && 'text' in option) {
      return option.text;
    }
    return String(option); // Fallback to string conversion
  };

  const handleSelectAnswer = (questionId: number, optionIndex: number) => {
    setSelectedOption({
      ...selectedOption,
      [questionId]: optionIndex
    });

    const option = currentTest.questions[questionId].options[optionIndex];
    const optionText = getOptionText(option);

    setUserAnswers({
      ...userAnswers,
      [questionId]: optionText
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

      // Ensure we're using the proper test ID format
      const testIdToSubmit = currentTest._id || currentTest.id || testId;

      const response = await fetchAPI('/api/evaluate_test', {
        method: 'POST',
        body: JSON.stringify({
          test_id: testIdToSubmit,
          answers: formattedAnswers
        }),
      });

      if (response.success) {
        setTestResults(response);
        if (response.attempt_history) {
          setAttemptHistory(response.attempt_history);
        }
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

  const handleDeleteTest = async () => {
    try {
      setLoading(true);

      const testIdToDelete = currentTest._id || testId;
      await fetchAPI(`/api/tests/${testIdToDelete}`, {
        method: 'DELETE'
      });

      // Redirect to tests page after deletion
      handleBackToTests();
    } catch (err: any) {
      const errorMessage = err.message || 'Error deleting test. Please try again.';
      setError(errorMessage);
      console.error('Error deleting test:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleBackToTests = () => {
    router.push('/tests');
  };

  // Format date for display
  const formatDate = (dateString: string) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleString();
    } catch (e) {
      return dateString;
    }
  };

  // Render test taking interface
  const renderTestInterface = () => {
    if (!currentTest) return null;

    return (
      <div className="container mx-auto p-4">
        <div className="flex justify-between mb-4">
          <Button
            color="light"
            className="dark:bg-gray-700 dark:text-white dark:hover:bg-gray-600"
            onClick={handleBackToTests}
          >
            <FiArrowLeft className="mr-2" /> Back to Tests
          </Button>

          <Button
            color="failure"
            onClick={handleDeleteTest}
            className="bg-red-600 hover:bg-red-700"
          >
            Delete Test
          </Button>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-md">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">{currentTest.title}</h1>
          <p className="text-gray-600 dark:text-gray-400 mb-6">Topic: {currentTest.topic}</p>

          {/* Show previous attempts if they exist */}
          {currentTest.attempts > 0 && (
            <div className="mb-6 p-4 bg-blue-50 dark:bg-blue-900 rounded-lg">
              <div className="flex items-center mb-3">
                <FiBarChart2 className="mr-2 text-blue-600 dark:text-blue-400" />
                <h3 className="text-lg font-medium text-blue-800 dark:text-blue-300">Test Performance</h3>
              </div>

              <div className="flex justify-between items-center mb-2">
                <span className="text-blue-700 dark:text-blue-300 font-medium">Highest Score:</span>
                <span className={`text-2xl font-bold ${
                  (currentTest.best_score || 0) >= 70 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'
                }`}>{currentTest.best_score || 0}%</span>
              </div>

              {/* Display previous scores */}
              {currentTest.attempt_history && currentTest.attempt_history.length > 0 && (
                <div className="mt-4 mb-2">
                  <p className="text-blue-700 dark:text-blue-300 font-medium mb-2">Previous Scores:</p>
                  <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-2">
                    {currentTest.attempt_history.map((attempt: AttemptHistory) => (
                      <div
                        key={attempt.attempt_id}
                        className={`text-center p-2 rounded-lg ${
                          attempt.score >= 70
                            ? 'bg-green-100 dark:bg-green-800'
                            : 'bg-blue-100 dark:bg-blue-800'
                        }`}
                      >
                        <div className={`text-lg font-bold ${
                          attempt.score >= 70
                            ? 'text-green-700 dark:text-green-300'
                            : 'text-blue-700 dark:text-blue-300'
                        }`}>
                          {attempt.score}%
                        </div>
                        <div className="text-xs text-gray-500 dark:text-gray-400">
                          {new Date(attempt.timestamp).toLocaleDateString()}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {currentTest.last_attempt_score && (
                <p className="text-blue-700 dark:text-blue-300">
                  Last Score: <span className="font-semibold">{currentTest.last_attempt_score}%</span>
                </p>
              )}
            </div>
          )}

          {currentTest.questions.map((question: any, qIndex: number) => (
            <div key={qIndex} className="mb-6 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg shadow-sm">
              <p className="font-medium mb-3 text-gray-900 dark:text-white">
                {qIndex + 1}. {question.text || question.question_text}
              </p>
              <div className="space-y-2">
                {question.options.map((option: any, oIndex: number) => (
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
                      {getOptionText(option)}
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
            className="w-full md:w-auto bg-indigo-600 hover:bg-indigo-700"
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
        <div className="flex justify-between mb-4">
          <Button
            color="light"
            className="dark:bg-gray-700 dark:text-white dark:hover:bg-gray-600"
            onClick={handleBackToTests}
          >
            <FiArrowLeft className="mr-2" /> Back to Tests
          </Button>

          <Button
            color="failure"
            onClick={handleDeleteTest}
            className="bg-red-600 hover:bg-red-700"
          >
            Delete Test
          </Button>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-md">
          <div className="text-center mb-6">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Test Results</h1>
            <h2 className="text-xl text-gray-700 dark:text-gray-300">{testResults.test_title}</h2>
            <div className="mt-4 text-3xl font-bold">
              <span className={testResults.score >= 70 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}>
                Score: {testResults.score}%
              </span>
            </div>

            {/* Display test history - highlight best score */}
            {testResults.attempt_history && testResults.attempt_history.length > 0 && (
              <div className="mt-6 mb-6 max-w-lg mx-auto">
                <h3 className="text-lg font-medium text-gray-800 dark:text-gray-200 mb-3">Score History</h3>
                <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
                    {testResults.attempt_history.map((attempt: AttemptHistory) => (
                      <div
                        key={attempt.attempt_id}
                        className={`p-3 rounded-lg text-center ${
                          attempt.score >= 70
                            ? 'bg-green-50 dark:bg-green-900'
                            : 'bg-gray-100 dark:bg-gray-600'
                        }`}
                      >
                        <div className={`text-xl font-bold ${
                          attempt.score >= 70
                            ? 'text-green-600 dark:text-green-400'
                            : 'text-gray-700 dark:text-gray-300'
                        }`}>
                          {attempt.score}%
                        </div>
                        <div className="text-xs text-gray-500 dark:text-gray-400">
                          {new Date(attempt.timestamp).toLocaleDateString()}
                        </div>
                      </div>
                    ))}
                  </div>
                  <div className="mt-4 pt-3 border-t dark:border-gray-600 flex justify-between">
                    <span className="font-medium text-gray-800 dark:text-gray-200">Best Score:</span>
                    <span className="font-bold text-blue-600 dark:text-blue-400">{testResults.best_score}%</span>
                  </div>
                </div>
              </div>
            )}
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
                    Question {index + 1}: {currentTest.questions[index].text || currentTest.questions[index].question_text}
                  </p>
                </div>
                <div className="ml-7">
                  <p className={`text-sm ${result.is_correct ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'} mb-1`}>
                    Your answer: {getOptionText(result.user_answer)}
                  </p>
                  <p className="text-sm text-green-600 dark:text-green-400 mb-2">
                    Correct answer: {getOptionText(result.correct_answer)}
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
            className="w-full md:w-auto mt-6 bg-indigo-600 hover:bg-indigo-700"
          >
            Back to Tests
          </Button>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100 dark:bg-gray-900">
        <Spinner size="xl" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-100 dark:bg-gray-900 p-4">
        <div className="p-4 bg-red-100 text-red-700 rounded-md mx-auto mt-4 max-w-lg">
          <h2 className="font-bold mb-2">Error</h2>
          <p>{error}</p>
          <Button
            color="light"
            className="mt-4"
            onClick={handleBackToTests}
          >
            <FiArrowLeft className="mr-2" /> Back to Tests
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900">
      {testResults ? renderTestResults() : renderTestInterface()}
    </div>
  );
}
