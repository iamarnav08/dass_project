'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { FiUser, FiLock, FiCheck, FiX, FiArrowLeft, FiSettings, FiTrash2 } from 'react-icons/fi';
import { authService } from '@/lib/auth';
import { FiCalendar, FiAward } from 'react-icons/fi';
import { format } from 'date-fns';

export default function ProfilePage() {
  const router = useRouter();
  const [username, setUsername] = useState('');
  const [grade, setGrade] = useState('11');
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showPasswordForm, setShowPasswordForm] = useState(false);
  const [showUsernameForm, setShowUsernameForm] = useState(false);
  const [showGradeForm, setShowGradeForm] = useState(false);
  // For clear activity feature
  const [showClearActivityForm, setShowClearActivityForm] = useState(false);
  const [clearActivityPassword, setClearActivityPassword] = useState('');
  const [clearingActivity, setClearingActivity] = useState(false);
  // For streaks
  const [currentStreak, setCurrentStreak] = useState(0);
  const [longestStreak, setLongestStreak] = useState(0);
  const [streakHistory, setStreakHistory] = useState<string[]>([]);
  // Modified to track multiple months
  const [calendarMonths, setCalendarMonths] = useState<Date[][]>([]);
  const [monthLabels, setMonthLabels] = useState<string[]>([]);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
      return;
    }

    // Generate calendar days for current month and previous months
    const generateCalendarMonths = () => {
      const today = new Date(); // Current date (April 2025)
      const months: Date[][] = [];
      const labels: string[] = [];
      
      // Generate data for current month and 2 previous months (total 3 months)
      for (let monthOffset = 0; monthOffset <= 2; monthOffset++) {
        const year = today.getFullYear();
        const month = today.getMonth() - monthOffset;
        
        // Create a date object for this month, handling year rollover correctly
        const targetDate = new Date(year, month, 1);
        
        // Get month name and year
        labels.push(format(targetDate, 'MMMM yyyy'));
        
        // Get the first day of the month
        const firstDay = new Date(targetDate.getFullYear(), targetDate.getMonth(), 1);
        // Get the last day of the month
        const lastDay = new Date(targetDate.getFullYear(), targetDate.getMonth() + 1, 0);
        
        // Get the day of week for first day (0 = Sunday, 6 = Saturday)
        const firstDayOfWeek = firstDay.getDay();
        
        // Create array for all days in the month view
        const days: Date[] = [];
        
        // Add days from previous month to fill the first week
        const prevMonthLastDay = new Date(targetDate.getFullYear(), targetDate.getMonth(), 0).getDate();
        for (let i = 0; i < firstDayOfWeek; i++) {
          const prevMonthDay = prevMonthLastDay - firstDayOfWeek + i + 1;
          days.push(new Date(targetDate.getFullYear(), targetDate.getMonth() - 1, prevMonthDay));
        }
        
        // Add all days from current month
        for (let i = 1; i <= lastDay.getDate(); i++) {
          days.push(new Date(targetDate.getFullYear(), targetDate.getMonth(), i));
        }
        
        // Calculate how many days we need to add from next month
        // We want a complete grid of 6 weeks (42 days)
        const remainingDays = 42 - days.length;
        
        // Add days from next month to complete the grid
        for (let i = 1; i <= remainingDays; i++) {
          days.push(new Date(targetDate.getFullYear(), targetDate.getMonth() + 1, i));
        }
        
        months.push(days);
      }
      
      // Set the months in reverse order (most recent first)
      setCalendarMonths(months.reverse());
      setMonthLabels(labels.reverse());
    };

    // Fetch user data
    const fetchUser = async () => {
      try {
        const user = await authService.getUser();
        if (user) {
          setUsername(user.username);
          // Set grade information
          if (user.grade) {
            setGrade(user.grade);
          }
          // Set streak information
          if (user.streak_data) {
            setCurrentStreak(user.streak_data.current_streak);
            setLongestStreak(user.streak_data.longest_streak);
            setStreakHistory(user.streak_data.streak_history || []);
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
    // Initialize calendar
    generateCalendarMonths();
  }, [router]);

  const handleUsernameChange = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch('http://localhost:5000/api/user/username', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ username })
      });

      if (!response.ok) {
        if (response.status === 401) {
          authService.handleTokenExpiration();
          return;
        }
        const data = await response.json();
        throw new Error(data.message || 'Failed to update username');
      }

      setSuccess('Username updated successfully');
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to update username');
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    if (newPassword !== confirmPassword) {
      setError('New passwords do not match');
      setLoading(false);
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/user/password', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword
        })
      });

      if (!response.ok) {
        if (response.status === 401) {
          authService.handleTokenExpiration();
          return;
        }
        const data = await response.json();
        throw new Error(data.message || 'Failed to update password');
      }

      setSuccess('Password updated successfully');
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
      setShowPasswordForm(false);
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to update password');
    } finally {
      setLoading(false);
    }
  };

  const handleGradeChange = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch('http://localhost:5000/api/user/grade', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ grade })
      });

      if (!response.ok) {
        if (response.status === 401) {
          authService.handleTokenExpiration();
          return;
        }
        const data = await response.json();
        throw new Error(data.message || 'Failed to update grade');
      }

      setSuccess('Grade updated successfully');
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to update grade');
    } finally {
      setLoading(false);
    }
  };

  const handleClearActivity = async () => {
    if (!clearActivityPassword) {
      setError('Password is required');
      return;
    }

    setClearingActivity(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch('http://localhost:5000/api/user/clear-activity', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ password: clearActivityPassword })
      });

      if (!response.ok) {
        if (response.status === 401) {
          setError('Incorrect password');
          return;
        }
        const data = await response.json();
        throw new Error(data.message || 'Failed to clear activity data');
      }

      setSuccess('All activity data has been cleared successfully');
      setShowClearActivityForm(false);
      setClearActivityPassword('');
      
      // Reset streaks in UI
      setCurrentStreak(0);
      setLongestStreak(0);
      setStreakHistory([]);
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to clear activity data');
    } finally {
      setClearingActivity(false);
    }
  };

  return (
    <div className="min-h-screen w-full bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <div className="border-b border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-800">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center">
              <button
                onClick={() => router.push('/chat')}
                className="mr-4 rounded-full p-2 text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700"
                aria-label="Back to chat"
              >
                <FiArrowLeft className="size-5" />
              </button>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Profile Settings</h1>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Two-column layout */}
        <div className="flex flex-col gap-8 lg:flex-row">
          {/* Left column - User Settings */}
          <div className="flex w-full flex-col space-y-4 lg:w-1/3">
            {/* User Info Card */}
            <div className="overflow-hidden rounded-lg bg-white shadow dark:bg-gray-800">
              <div className="p-4">
                <div className="flex items-center">
                  <div className="flex size-12 items-center justify-center rounded-full bg-indigo-600">
                    <FiUser className="size-6 text-white" />
                  </div>
                  <div className="ml-4">
                    <h2 className="text-lg font-semibold text-gray-900 dark:text-white">{username}</h2>
                    <p className="text-xs text-gray-500 dark:text-gray-400">Manage your account settings</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Username Change Form */}
            <div className="overflow-hidden rounded-lg bg-white shadow dark:bg-gray-800">
              <div className="border-b border-gray-200 p-4 dark:border-gray-700">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-base font-medium text-gray-900 dark:text-white">Username Settings</h2>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      Update your display name
                    </p>
                  </div>
                  {!showUsernameForm ? (
                    <button
                      onClick={() => setShowUsernameForm(true)}
                      className="rounded-md bg-indigo-600 px-2 py-1.5 text-xs font-medium text-white hover:bg-indigo-700 focus:outline-none"
                    >
                      Update Username
                    </button>
                  ) : (
                    <button
                      onClick={() => setShowUsernameForm(false)}
                      className="text-xs font-medium text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300"
                    >
                      Cancel
                    </button>
                  )}
                  <div className="flex size-8 items-center justify-center rounded-full bg-indigo-100 dark:bg-indigo-900">
                    <FiUser className="size-4 text-indigo-600 dark:text-indigo-400" />
                  </div>
                </div>
              </div>
              {showUsernameForm && (
                <div className="p-4">
                  <form onSubmit={handleUsernameChange} className="space-y-3">
                    <div>
                      <label htmlFor="username" className="block text-xs font-medium text-gray-700 dark:text-gray-300">
                        Username
                      </label>
                      <div className="mt-1">
                        <input
                          type="text"
                          id="username"
                          value={username}
                          onChange={(e) => setUsername(e.target.value)}
                          className="block w-full rounded-md border border-gray-300 px-3 py-1.5 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                          required
                        />
                      </div>
                    </div>
                    <button
                      type="submit"
                      disabled={loading}
                      className="inline-flex w-full justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-1.5 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50"
                    >
                      {loading ? 'Updating...' : 'Update Username'}
                    </button>
                  </form>
                </div>
              )}
            </div>

            {/* Grade Change Form */}
            <div className="overflow-hidden rounded-lg bg-white shadow dark:bg-gray-800">
              <div className="border-b border-gray-200 p-4 dark:border-gray-700">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-base font-medium text-gray-900 dark:text-white">Grade Settings</h2>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      Select your current grade
                    </p>
                  </div>
                  {!showGradeForm ? (
                    <button
                      onClick={() => setShowGradeForm(true)}
                      className="rounded-md bg-indigo-600 px-2 py-1.5 text-xs font-medium text-white hover:bg-indigo-700 focus:outline-none"
                    >
                      Update Grade
                    </button>
                  ) : (
                    <button
                      onClick={() => setShowGradeForm(false)}
                      className="text-xs font-medium text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300"
                    >
                      Cancel
                    </button>
                  )}
                  <div className="flex size-8 items-center justify-center rounded-full bg-indigo-100 dark:bg-indigo-900">
                    <FiAward className="size-4 text-indigo-600 dark:text-indigo-400" />
                  </div>
                </div>
              </div>
              {showGradeForm && (
                <div className="p-4">
                  <form onSubmit={handleGradeChange} className="space-y-3">
                    <div>
                      <label htmlFor="grade" className="block text-xs font-medium text-gray-700 dark:text-gray-300">
                        Grade
                      </label>
                      <div className="mt-1">
                        <select 
                          id="grade"
                          value={grade}
                          onChange={(e) => setGrade(e.target.value)}
                          className="block w-full rounded-md border border-gray-300 px-3 py-1.5 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                          required
                        >
                          <option value="10">Grade 10</option>
                          <option value="11">Grade 11</option>
                          <option value="12">Grade 12</option>
                        </select>
                      </div>
                    </div>
                    <button
                      type="submit"
                      disabled={loading}
                      className="inline-flex w-full justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-1.5 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50"
                    >
                      {loading ? 'Updating...' : 'Update Grade'}
                    </button>
                  </form>
                </div>
              )}
            </div>

            {/* Password Settings */}
            <div className="overflow-hidden rounded-lg bg-gray-800 shadow">
              <div className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-base font-medium text-gray-900 dark:text-white">Password Settings</h2>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      Set New Password securely
                    </p>
                  </div>
                  {!showPasswordForm ? (
                    <button
                      onClick={() => setShowPasswordForm(true)}
                      className="rounded-md bg-indigo-600 px-2 py-1.5 text-xs font-medium text-white hover:bg-indigo-700 focus:outline-none"
                    >
                      Update Password
                    </button>
                  ) : (
                    <button
                      onClick={() => setShowPasswordForm(false)}
                      className="text-xs font-medium text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300"
                    >
                      Cancel
                    </button>
                  )}
                  <div className="flex size-8 items-center justify-center rounded-full bg-indigo-100 dark:bg-indigo-900">
                    <FiLock className="size-4 text-indigo-600 dark:text-indigo-400" />
                  </div>
                </div>
                
                {showPasswordForm && (
                  <div className="p-4">
                    <form onSubmit={handlePasswordChange} className="space-y-3">
                      <div>
                        <label htmlFor="currentPassword" className="block text-xs font-medium text-gray-700 dark:text-gray-300">
                          Current Password
                        </label>
                        <div className="mt-1">
                          <input
                            type="password"
                            id="currentPassword"
                            value={currentPassword}
                            onChange={(e) => setCurrentPassword(e.target.value)}
                            className="block w-full rounded-md border border-gray-300 px-3 py-1.5 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                            required
                          />
                        </div>
                      </div>

                      <div>
                        <label htmlFor="newPassword" className="block text-xs font-medium text-gray-700 dark:text-gray-300">
                          New Password
                        </label>
                        <div className="mt-1">
                          <input
                            type="password"
                            id="newPassword"
                            value={newPassword}
                            onChange={(e) => setNewPassword(e.target.value)}
                            className="block w-full rounded-md border border-gray-300 px-3 py-1.5 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                            required
                          />
                        </div>
                      </div>

                      <div>
                        <label htmlFor="confirmPassword" className="block text-xs font-medium text-gray-700 dark:text-gray-300">
                          Confirm New Password
                        </label>
                        <div className="mt-1">
                          <input
                            type="password"
                            id="confirmPassword"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            className="block w-full rounded-md border border-gray-300 px-3 py-1.5 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                            required
                          />
                        </div>
                      </div>

                      <button
                        type="submit"
                        disabled={loading}
                        className="inline-flex w-full justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-1.5 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50"
                      >
                        {loading ? 'Updating...' : 'Update Password'}
                      </button>
                    </form>
                  </div>
                )}
              </div>
            </div>

            {/* Clear Activity Data */}
            <div className="overflow-hidden rounded-lg bg-red-900 shadow">
              <div className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-base font-medium text-white">Clear Activity Data</h2>
                    <p className="text-xs text-gray-300">
                      Reset all your Activity and Chat History
                    </p>
                  </div>
                  {!showClearActivityForm ? (
                    <button
                      onClick={() => setShowClearActivityForm(true)}
                      className="rounded-md bg-red-600 px-2 py-1.5 text-xs font-medium text-white hover:bg-red-700 focus:outline-none"
                    >
                      Clear Data
                    </button>
                  ) : (
                    <button
                      onClick={() => setShowClearActivityForm(false)}
                      className="text-xs font-medium text-red-200 hover:text-red-100"
                    >
                      Cancel
                    </button>
                  )}
                  <div className="flex size-8 items-center justify-center rounded-full bg-red-800">
                    <FiTrash2 className="size-4 text-red-200" />
                  </div>
                </div>
                
                {showClearActivityForm && (
                  <div className="p-4">
                    <form onSubmit={handleClearActivity} className="space-y-3">
                      <div>
                        <label htmlFor="clearActivityPassword" className="block text-xs font-medium text-gray-300">
                          Enter your password to confirm
                        </label>
                        <div className="mt-1">
                          <input
                            type="password"
                            id="clearActivityPassword"
                            value={clearActivityPassword}
                            onChange={(e) => setClearActivityPassword(e.target.value)}
                            className="block w-full rounded-md border border-gray-600 px-3 py-1.5 text-sm shadow-sm focus:border-red-500 focus:outline-none focus:ring-1 focus:ring-red-500 dark:bg-gray-700 dark:text-white"
                            required
                          />
                        </div>
                      </div>

                      <button
                        type="submit"
                        disabled={clearingActivity}
                        className="inline-flex w-full justify-center rounded-md border border-transparent bg-red-600 px-4 py-1.5 text-sm font-medium text-white shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 disabled:opacity-50"
                      >
                        {clearingActivity ? 'Clearing...' : 'Clear Data'}
                      </button>
                    </form>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Right column - Activity */}
          <div className="w-full lg:w-2/3">
            {/* Streak Information */}
            <div className="overflow-hidden rounded-lg bg-white shadow dark:bg-gray-800">
              <div className="border-b border-gray-200 p-6 dark:border-gray-700">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-lg font-medium text-gray-900 dark:text-white">Activity</h2>
                    <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                      Interaction History
                    </p>
                  </div>
                  <div className="flex size-10 items-center justify-center rounded-full bg-indigo-100 dark:bg-indigo-900">
                    <FiCalendar className="size-5 text-indigo-600 dark:text-indigo-400" />
                  </div>
                </div>
              </div>
              
              <div className="p-6">
                <div className="mb-6 flex items-center justify-between">
                  <div className="flex-1 text-center">
                    <div className="text-3xl font-bold text-indigo-600">{currentStreak}</div>
                    <div className="text-sm text-gray-500">Current Streak</div>
                  </div>
                  <div className="flex-1 text-center">
                    <div className="text-3xl font-bold text-indigo-600">{longestStreak}</div>
                    <div className="text-sm text-gray-500">Longest Streak</div>
                  </div>
                </div>
                
                {/* Activity Calendar */}
                <div className="mt-4">
                  <h3 className="mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">Activity Calendar</h3>
                  <div className="w-full">
                    <div className="mb-4">
                      <div className="flex justify-between">
                        {calendarMonths.slice(0, 3).map((month, monthIndex) => (
                          <div key={monthIndex} className="w-[31%]">
                            <div className="mb-2">
                              <span className="text-xs font-medium text-gray-500 dark:text-gray-400">
                                {monthLabels[monthIndex]}
                              </span>
                            </div>
                            <div className="mb-1 grid grid-cols-7">
                              {['S', 'M', 'T', 'W', 'T', 'F', 'S'].map((day, index) => (
                                <div key={index} className="flex justify-center text-center text-sm text-gray-400">
                                  {day}
                                </div>
                              ))}
                            </div>
                            <div className="grid grid-cols-7 gap-[2px]">
                              {month.map((date, i) => {
                                const dateStr = format(date, 'yyyy-MM-dd');
                                const isActive = streakHistory.includes(dateStr);
                                const isCurrentMonth = date.getMonth() === new Date(monthLabels[monthIndex]).getMonth();
                                
                                return (
                                  <div 
                                    key={i}
                                    className={`size-6 rounded-md ${
                                      isActive 
                                        ? 'bg-indigo-600 dark:bg-indigo-500'
                                        : isCurrentMonth
                                          ? 'bg-gray-600 dark:bg-gray-700'
                                          : 'bg-gray-700 dark:bg-gray-800'
                                    }`}
                                    title={format(date, 'MMMM d, yyyy')}
                                  />
                                );
                              })}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                    <div className="mt-2 flex items-center">
                      <span className="mr-1 text-xs text-gray-500 dark:text-gray-400">Less</span>
                      <div className="flex space-x-1">
                        <div className="size-3 rounded-sm bg-gray-300 dark:bg-gray-700"></div>
                        <div className="size-3 rounded-sm bg-indigo-400 dark:bg-indigo-700"></div>
                        <div className="size-3 rounded-sm bg-indigo-500 dark:bg-indigo-600"></div>
                        <div className="size-3 rounded-sm bg-indigo-600 dark:bg-indigo-500"></div>
                      </div>
                      <span className="ml-1 text-xs text-gray-500 dark:text-gray-400">More</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Status Messages */}
        {(error || success) && (
          <div className="mt-4">
            {error && (
              <div className="rounded-md bg-red-50 p-4 text-sm text-red-700 dark:bg-red-900 dark:text-red-200">
                <div className="flex">
                  <div className="shrink-0">
                    <FiX className="size-5" />
                  </div>
                  <div className="ml-3">{error}</div>
                </div>
              </div>
            )}
            {success && (
              <div className="rounded-md bg-green-50 p-4 text-sm text-green-700 dark:bg-green-900 dark:text-green-200">
                <div className="flex">
                  <div className="shrink-0">
                    <FiCheck className="size-5" />
                  </div>
                  <div className="ml-3">{success}</div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}