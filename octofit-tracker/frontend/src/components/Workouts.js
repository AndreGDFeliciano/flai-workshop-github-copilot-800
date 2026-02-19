import React, { useState, useEffect } from 'react';

const Workouts = () => {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;

  useEffect(() => {
    console.log('Fetching workouts from:', API_URL);
    
    fetch(API_URL)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts API response:', data);
        // Handle both paginated (.results) and plain array responses
        const workoutsList = data.results || data;
        console.log('Processed workouts data:', workoutsList);
        setWorkouts(workoutsList);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching workouts:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [API_URL]);

  const getIntensityBadge = (difficulty) => {
    const badges = {
      'beginner': 'success',
      'intermediate': 'warning',
      'advanced': 'danger',
      'elite': 'danger'
    };
    return badges[difficulty] || 'secondary';
  };

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="loading-spinner">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3">Loading workouts...</p>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="container mt-4">
        <div className="alert alert-danger error-message" role="alert">
          <h4 className="alert-heading">Error!</h4>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="page-header">
        <h2>💪 Workout Suggestions</h2>
        <p>Personalized workout recommendations to help you achieve your fitness goals</p>
      </div>
      
      <div className="mb-3">
        <h5>Available Workouts: <span className="badge bg-primary">{workouts.length}</span></h5>
      </div>

      <div className="row">
        {workouts.map(workout => (
          <div key={workout._id} className="col-md-6 col-lg-4 mb-4">
            <div className="card h-100">
              <div className="card-header bg-primary text-white">
                <h5 className="card-title mb-0">{workout.name}</h5>
                <small><span className="badge bg-light text-dark">{workout.difficulty}</span></small>
              </div>
              <div className="card-body">
                <p className="card-text">{workout.description}</p>
                <div className="d-flex flex-wrap gap-2 mb-3">
                  <span className="badge bg-info">⏱️ {workout.duration_minutes} min</span>
                  <span className={`badge bg-${getIntensityBadge(workout.difficulty)}`}>
                    🔥 {workout.difficulty}
                  </span>
                  <span className="badge bg-secondary">📊 {workout.exercises?.length || 0} exercises</span>
                </div>
              </div>
              <div className="card-footer bg-light">
                <div className="d-flex justify-content-between align-items-center">
                  <span className="text-muted"><strong>Est. Points:</strong></span>
                  <span className="badge bg-primary fs-6">{workout.points}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Workouts;
