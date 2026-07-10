import React, { useEffect, useMemo, useState } from 'react';
import './App.css';

// const BASE_URL = 'http://127.0.0.1:5000';

function PlusIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M11 5h2v6h6v2h-6v6h-2v-6H5v-2h6z" />
    </svg>
  );
}

function GearIcon({ spinning = false }) {
  return (
    <svg viewBox="0 0 24 24" className={spinning ? 'icon-spin' : ''} aria-hidden="true">
      <path d="M19.14 12.94a7.94 7.94 0 0 0 .05-.94 7.94 7.94 0 0 0-.05-.94l2.03-1.58a.5.5 0 0 0 .12-.64l-1.92-3.32a.5.5 0 0 0-.6-.22l-2.39.96a7.87 7.87 0 0 0-1.63-.94L14.4 2.5a.5.5 0 0 0-.5-.42h-3.84a.5.5 0 0 0-.5.42l-.38 2.56a7.87 7.87 0 0 0-1.63.94l-2.39-.96a.5.5 0 0 0-.6.22L1.71 10.72a.5.5 0 0 0 .12.64l2.03 1.58a7.94 7.94 0 0 0-.05.94 7.94 7.94 0 0 0 .05.94L1.83 14.5a.5.5 0 0 0-.12.64l1.92 3.32a.5.5 0 0 0 .6.22l2.39-.96c.5.4 1.03.73 1.63.94l.38 2.56a.5.5 0 0 0 .5.42h3.84a.5.5 0 0 0 .5-.42l.38-2.56c.6-.21 1.13-.54 1.63-.94l2.39.96a.5.5 0 0 0 .6-.22l1.92-3.32a.5.5 0 0 0-.12-.64zM12 15.5A3.5 3.5 0 1 1 12 8.5a3.5 3.5 0 0 1 0 7z" />
    </svg>
  );
}

function FolderIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M4 6.5A2.5 2.5 0 0 1 6.5 4h3.1a1.5 1.5 0 0 1 1.12.47l1.26 1.38h5.52A2.5 2.5 0 0 1 20 8.35v8.15A2.5 2.5 0 0 1 17.5 19h-11A2.5 2.5 0 0 1 4 16.5z" />
    </svg>
  );
}

function ArrowRightIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M13.17 5.17 18 10h-10v2h10l-4.83 4.83 1.41 1.41L21 11l-6.42-6.42z" />
    </svg>
  );
}

function ArrowLeftIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z" />
    </svg>
  );
}

function FileIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M6 2h8l4 4v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2zm7 1.5V7h3.5z" />
    </svg>
  );
}

function TrashIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M9 3h6l1 2h4v2H4V5h4zM6 8h12l-1 12H7z" />
    </svg>
  );
}

function DownloadIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 3l5 5h-3v6h-4V8H7zM5 16h14v2H5z" />
    </svg>
  );
}

function MoreIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M5 10a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm7 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm7 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4z" />
    </svg>
  );
}

function SearchIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M10.5 4a6.5 6.5 0 1 1 0 13 6.5 6.5 0 0 1 0-13zm8.5 13 2 2-1.4 1.4-2-2z" />
    </svg>
  );
}

function KeyIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M7 10a4 4 0 1 1 3.87 4.87L11 15h2v2h2v2h2l1.5-1.5-1.5-1.5-1.5 1.5L13.5 16H12l-.13-.13A4 4 0 0 1 7 10z" />
    </svg>
  );
}

function CopyIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M8 4h9a2 2 0 0 1 2 2v9h-2V6H8zM6 8h9a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2z" />
    </svg>
  );
}

function CloseIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M6.4 5 5 6.4 10.6 12 5 17.6 6.4 19 12 13.4 17.6 19 19 17.6 13.4 12 19 6.4 17.6 5 12 10.6z" />
    </svg>
  );
}

function UserIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 12a4 4 0 1 0-4-4 4 4 0 0 0 4 4zm0 2c-4.42 0-8 2.24-8 5v1h16v-1c0-2.76-3.58-5-8-5z" />
    </svg>
  );
}

function LogoutIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M16 4h2a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-2v-2h2V6h-2zM10 7l5 5-5 5v-3H4V10h6z" />
    </svg>
  );
}

export default function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || null);
  const [userId, setUserId] = useState(localStorage.getItem('userId') || null);
  const [userEmail, setUserEmail] = useState('');

  const [authView, setAuthView] = useState('login');
  const [profileDropdown, setProfileDropdown] = useState(false);
  const [rightPanelContent, setRightPanelContent] = useState('default');

  // Responsiveness tracking overlay vector
  const [mobileActiveColumn, setMobileActiveColumn] = useState('first');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const [currentStep, setCurrentStep] = useState(1);
  const [csvFile, setCsvFile] = useState(null);
  const [csvColumns, setCsvColumns] = useState([]);
  const [isInspecting, setIsInspecting] = useState(false);
  const [inspectStatusText, setInspectStatusText] = useState('');
  const [modelName, setModelName] = useState('');
  const [selectedTarget, setSelectedTarget] = useState('');
  const [selectedFeatures, setSelectedFeatures] = useState([]);

  // Operational feedback states
  const [isAuthLoading, setIsAuthLoading] = useState(false);
  const [isCopying, setIsCopying] = useState({ key: false, url: false, instructions: false });
  const [isDragOver, setIsDragOver] = useState(false);

  const [myModels, setMyModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState(null);
  const [showModelsModal, setShowModelsModal] = useState(false);
  const [activeModal, setActiveModal] = useState(null);
  const [sampleMenuOpen, setSampleMenuOpen] = useState(false);
  const [detailsMenuOpen, setDetailsMenuOpen] = useState(null);
  const [showOperationsPanel, setShowOperationsPanel] = useState(false);

  // Dynamic user prediction interface states
  const [predictInputs, setPredictInputs] = useState({});
  const [predictionResult, setPredictionResult] = useState(null);
  const [isPredictingLoading, setIsPredictingLoading] = useState(false);

  // Running workflows collection array
  const [runningOperations, setRunningOperations] = useState([]);
  const [operationIndex, setOperationIndex] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');
  const [appliedSearch, setAppliedSearch] = useState('');

  const [authEmail, setAuthEmail] = useState('');
  const [authPassword, setAuthPassword] = useState('');
  const [authConfirmPassword, setAuthConfirmPassword] = useState('');
  const [authOtp, setAuthOtp] = useState('');

  useEffect(() => {
    if (token && userId) {
      fetchProfileDetails();
      fetchCloudModels();
    }
  }, [token, userId]);

  // Clean prediction buffers cleanly whenever the target active modal focus resets
  useEffect(() => {
    if (!activeModal) {
      setPredictInputs({});
      setPredictionResult(null);
      setIsPredictingLoading(false);
    }
  }, [activeModal]);

  const BASE_URL = import.meta.env.VITE_API_URL || '';

  const fetchProfileDetails = async () => {
    try {
      const res = await fetch(`${BASE_URL}/api/auth/me`, { headers: { Authorization: `Bearer ${token}` } });
      if (res.ok) {
        const data = await res.json();
        setUserEmail(data.user?.email || '');
      } else {
        handleLogout();
      }
    } catch (error) {
      console.error(error);
    }
  };

  const fetchCloudModels = async () => {
    try {
      const res = await fetch(`${BASE_URL}/api/developer/models?user_id=${userId}`);
      if (res.ok) {
        const data = await res.json();
        setMyModels(data.models || []);
      }
    } catch (error) {
      console.error(error);
    }
  };

  const handleLogout = () => {
    localStorage.clear();
    setToken(null);
    setUserId(null);
    setRightPanelContent('default');
    setSelectedModel(null);
    setProfileDropdown(false);
    setMobileActiveColumn('first');
  };

  const handleFeatureToggle = (column) => {
    setSelectedFeatures((current) =>
      current.includes(column) ? current.filter((item) => item !== column) : [...current, column]
    );
  };

  const resetWizard = () => {
    setCurrentStep(1);
    setCsvFile(null);
    setCsvColumns([]);
    setSelectedTarget('');
    setSelectedFeatures([]);
    setModelName('');
    setShowOperationsPanel(false);
    setOperationIndex(0);
  };

  const openModelsPanel = () => {
    setRightPanelContent('models');
    setShowModelsModal(false);
    setProfileDropdown(false);
    setMobileActiveColumn('second'); 
  };

  const visibleModels = useMemo(() => {
    const query = appliedSearch.trim().toLowerCase();
    if (!query) return myModels;
    return myModels.filter((model) => model.model_name?.toLowerCase().includes(query));
  }, [appliedSearch, myModels]);

  // Secure array validation mapping logic to isolate feature tokens cleanly
  const currentModelFeatures = useMemo(() => {
    if (!selectedModel?.features) return [];
    if (Array.isArray(selectedModel.features)) return selectedModel.features;
    try {
      return JSON.parse(selectedModel.features);
    } catch (e) {
      return [];
    }
  }, [selectedModel]);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      const file = files[0];
      if (file.name.endsWith('.csv')) {
        setCsvFile(file);
      } else {
        alert('Please drop a valid .csv dataset file.');
      }
    }
  };

  const handleInspectFile = async () => {
    if (!csvFile || isInspecting) return;
    setIsInspecting(true);
    setInspectStatusText('Inspecting file...');
    const formData = new FormData();
    formData.append('file', csvFile);

    try {
      const res = await fetch(`${BASE_URL}/api/inspect-csv`, { method: 'POST', body: formData });
      if (res.ok) {
        const data = await res.json();
        setCsvColumns(data.columns || []);
        setInspectStatusText('Columns ready.');
      }
    } catch (error) {
      console.error(error);
      setInspectStatusText('Inspection failed.');
    } finally {
      setIsInspecting(false);
    }
  };

  const handleGenerateModel = async () => {
    if (!csvFile || !selectedTarget || selectedFeatures.length === 0 || isInspecting) return;
    setIsInspecting(true);
    setInspectStatusText('Training model...');
    const formData = new FormData();
    formData.append('file', csvFile);
    formData.append('model_name', modelName);
    formData.append('user_id', userId);
    formData.append('targets', selectedTarget);
    selectedFeatures.forEach((feature) => formData.append('features', feature));

    try {
      const res = await fetch(`${BASE_URL}/api/targets-features-train`, { method: 'POST', body: formData });
      if (res.ok) {
        setRunningOperations((current) => [
          { id: Date.now(), label: modelName || 'New model' },
          ...current,
        ]);
        setShowOperationsPanel(true);
        setOperationIndex(0);
        fetchCloudModels();
        resetWizard();
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsInspecting(false);
    }
  };

  const handleCopyText = (text, targetKey) => {
    setIsCopying(prev => ({ ...prev, [targetKey]: true }));
    navigator.clipboard.writeText(text);
    setTimeout(() => {
      setIsCopying(prev => ({ ...prev, [targetKey]: false }));
    }, 2000);
  };

  const toggleOperationsPanel = () => {
    if (!showOperationsPanel) {
      setShowOperationsPanel(true);
      setOperationIndex(0);
      return;
    }
    if (runningOperations.length > 1) {
      setOperationIndex((current) => (current + 1) % runningOperations.length);
    }
  };

  useEffect(() => {
    let intervalId;

    const syncRunningOperations = async () => {
      if (!userId || !token) return;
      try {
        const res = await fetch(`${BASE_URL}/api/developer/active-jobs?user_id=${userId}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        if (res.ok) {
          const data = await res.json();
          setRunningOperations(data.active_jobs || []);
        }
      } catch (error) {
        console.error("Operational sync failure:", error);
      }
    };

    if (token && userId) {
      syncRunningOperations();
      intervalId = setInterval(syncRunningOperations, 3000);
    }

    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [token, userId]);

  const handleTerminateOperation = async () => {
    const currentJob = runningOperations[operationIndex];
    if (!currentJob) return;

    if (!window.confirm(`Are you sure you want to terminate: ${currentJob.label}?`)) {
      return;
    }

    try {
      const res = await fetch(`${BASE_URL}/api/targets-features-cancel`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          job_id: currentJob.id,
          user_id: userId
        })
      });

      if (res.ok) {
        alert("Termination signal acknowledged by engine.");
        setRunningOperations(prev => prev.filter(job => job.id !== currentJob.id));
        setOperationIndex(0);
        setShowOperationsPanel(false);
        setCurrentStep(1);
      } else {
        alert("Failed to terminate the engine instance.");
      }
    } catch (error) {
      console.error("Termination communication error:", error);
    }
  };

  const handlePredictInputValueChange = (featureName, value) => {
    setPredictInputs(prev => ({
      ...prev,
      [featureName]: value
    }));
  };

  const handleExecutePrediction = async (e) => {
    e.preventDefault();
    if (!selectedModel?.api_key || isPredictingLoading) return;

    setIsPredictingLoading(true);
    setPredictionResult(null);

    try {
      const res = await fetch(`${BASE_URL}/api/v1/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${selectedModel.api_key}`
        },
        body: JSON.stringify(predictInputs)
      });

      const data = await res.json();
      if (res.ok) {
        setPredictionResult({ success: true, value: data.prediction });
      } else {
        setPredictionResult({ success: false, error: data.error || "Inference parsing failed." });
      }
    } catch (err) {
      console.error("API inference runtime block fault:", err);
      setPredictionResult({ success: false, error: "Unable to establish communication gateway with engine." });
    } finally {
      setIsPredictingLoading(false);
    }
  };

  if (!token) {
    return (
      <div className="app-shell auth-shell">
        <div className="auth-card">
          <div className="auth-header">
            <div className="brand-badge">A</div>
            <h1>AutoML Engine Arena</h1>
            <p>
              {authView === 'login' && 'Log in to your workspace'}
              {authView === 'signup' && 'Create your account'}
              {authView === 'forgot' && 'Recover your account'}
              {authView === 'otp' && 'Verify your reset code'}
            </p>
          </div>

          {authView === 'login' && (
            <div className="auth-form">
              <input type="email" disabled={isAuthLoading} placeholder="Email address" value={authEmail} onChange={(e) => setAuthEmail(e.target.value)} />
              <input type="password" disabled={isAuthLoading} placeholder="Password" value={authPassword} onChange={(e) => setAuthPassword(e.target.value)} />
              <button className="button button-primary" disabled={isAuthLoading} onClick={async () => {
                setIsAuthLoading(true);
                try {
                  const res = await fetch(`${BASE_URL}/api/auth/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: authEmail, password: authPassword }),
                  });
                  if (res.ok) {
                    const data = await res.json();
                    localStorage.setItem('token', data.access_token);
                    localStorage.setItem('userId', data.user_id);
                    setToken(data.access_token);
                    setUserId(data.user_id);
                  } else {
                    alert('Authentication rejected.');
                  }
                } catch (err) {
                  console.error(err);
                } finally {
                  setIsAuthLoading(false);
                }
              }}>
                {isAuthLoading ? 'Signing in...' : 'Sign in'}
              </button>
              <button className="link-button" disabled={isAuthLoading} onClick={() => setAuthView('forgot')}>Forgot password?</button>
              <p className="auth-switch">
                Need an account? <button disabled={isAuthLoading} onClick={() => setAuthView('signup')}>Create one</button>
              </p>
            </div>
          )}

          {authView === 'signup' && (
            <div className="auth-form">
              <input type="email" disabled={isAuthLoading} placeholder="Email address" value={authEmail} onChange={(e) => setAuthEmail(e.target.value)} />
              <input type="password" disabled={isAuthLoading} placeholder="Create password" value={authPassword} onChange={(e) => setAuthPassword(e.target.value)} />
              <input type="password" disabled={isAuthLoading} placeholder="Confirm password" value={authConfirmPassword} onChange={(e) => setAuthConfirmPassword(e.target.value)} />
              <button className="button button-primary" disabled={isAuthLoading} onClick={async () => {
                if (authPassword !== authConfirmPassword) {
                  alert('Passwords do not match.');
                  return;
                }
                setIsAuthLoading(true);
                try {
                  const res = await fetch(`${BASE_URL}/api/auth/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: authEmail, password: authPassword }),
                  });
                  if (res.ok) {
                    alert('Registration complete!');
                    setAuthView('login');
                  }
                } catch (err) {
                  console.error(err);
                } finally {
                  setIsAuthLoading(false);
                }
              }}>
                {isAuthLoading ? 'Creating account...' : 'Create account'}
              </button>
              <p className="auth-switch">
                Already registered? <button disabled={isAuthLoading} onClick={() => setAuthView('login')}>Log in</button>
              </p>
            </div>
          )}

          {authView === 'forgot' && (
            <div className="auth-form">
              <p className="helper-text">Enter your email address to receive a verification code.</p>
              <input type="email" disabled={isAuthLoading} placeholder="Email address" value={authEmail} onChange={(e) => setAuthEmail(e.target.value)} />
              <button className="button button-primary" disabled={isAuthLoading} onClick={async () => {
                setIsAuthLoading(true);
                try {
                  await fetch(`${BASE_URL}/api/auth/forgot-password`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email: authEmail }) });
                  setAuthView('otp');
                } catch (err) {
                  console.error(err);
                } finally {
                  setIsAuthLoading(false);
                }
              }}>
                {isAuthLoading ? 'Sending...' : 'Send code'}
              </button>
              <button className="button button-secondary" disabled={isAuthLoading} onClick={() => setAuthView('login')}>Back</button>
            </div>
          )}

          {authView === 'otp' && (
            <div className="auth-form">
              <input type="text" disabled={isAuthLoading} placeholder="Enter 6-digit code" value={authOtp} onChange={(e) => setAuthOtp(e.target.value)} />
              <input type="password" disabled={isAuthLoading} placeholder="New password" value={authPassword} onChange={(e) => setAuthPassword(e.target.value)} />
              <button className="button button-primary" disabled={isAuthLoading} onClick={async () => {
                setIsAuthLoading(true);
                try {
                  const res = await fetch(`${BASE_URL}/api/auth/reset-password-otp`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: authEmail, otp: authOtp, new_password: authPassword }),
                  });
                  if (res.ok) {
                    alert('Credentials reset successfully!');
                    setAuthView('login');
                  } else {
                    alert('Validation mismatch.');
                  }
                } catch (err) {
                  console.error(err);
                } finally {
                  setIsAuthLoading(false);
                }
              }}>
                {isAuthLoading ? 'Updating...' : 'Update password'}
              </button>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className={`app-shell dashboard-shell mobile-view-${mobileActiveColumn}`}>
      {/* COLUMN 1: WIZARD OPERATIONS */}
      <section className="panel panel-left">
        <div className="panel-header-sticky">
          <div className="topbar-nav">
            <div className="brand-inline">
              <div className="brand-badge">A</div>
              <div>
                <h2>AutoML Engine</h2>
                <p>Build and deploy models</p>
              </div>
            </div>

            <div className="nav-links desktop-nav">
              <button className="nav-link">About</button>
              <button className="nav-link">Help</button>
              <button className="nav-link">Contact</button>
            </div>

            <div className="mobile-nav-dropdown-container">
              <button
                className="icon-button mobile-menu-toggle-btn"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                aria-label="Toggle Navigation Menu"
              >
                ☰
              </button>
              {mobileMenuOpen && (
                <div className="mobile-dropdown-overlay-menu">
                  <button onClick={() => { setMobileActiveColumn('first'); setMobileMenuOpen(false); }}>Workspace Form</button>
                  <button onClick={() => { openModelsPanel(); setMobileMenuOpen(false); }}>My Models ({myModels.length})</button>
                  <div className="dropdown-divider"></div>
                  <button onClick={() => setMobileMenuOpen(false)}>About</button>
                  <button onClick={() => setMobileMenuOpen(false)}>Help</button>
                  <button onClick={() => setMobileMenuOpen(false)}>Contact</button>
                </div>
              )}
            </div>
          </div>

          <div className="wizard-actions-row">
            <button className="button button-primary action-button action-button-large" disabled={isInspecting} onClick={resetWizard}>
              <span className="action-icon"><PlusIcon /></span>
              <span className="action-divider" />
              <span>Add new model</span>
            </button>
            <button className="button action-button action-button-small" onClick={toggleOperationsPanel}>
              <span className="action-label">Running</span>
              <span className="action-ellipsis">…</span>
              <span className="action-divider" />
              <span>{runningOperations.length}</span>
              <span className="action-icon right-icon"><ArrowRightIcon /></span>
            </button>
          </div>
        </div>

        <div className="scrollable-container">
          <div className="wizard-card">
            <div className="wizard-head">
              <h3>{showOperationsPanel ? 'Operational Monitor' : 'Create your model'}</h3>
              <div className="divider-fade" />
            </div>

            {showOperationsPanel ? (
              <div className="step-block operations-panel">
                <h3>Running operations</h3>

                {runningOperations.length === 0 ? (
                  <div className="empty-operations-state">
                    <div className="empty-operations-icon">
                      <FileIcon />
                    </div>
                    <p>No running operations currently.</p>
                  </div>
                ) : (
                  <div className="operation-card">
                    <div className="operation-badge">Live</div>
                    <div>
                      <strong>{runningOperations[operationIndex]?.label}</strong>
                      <p>Your training workload is currently in progress.</p>
                      <span className="operation-index-indicator">
                        Job {operationIndex + 1} of {runningOperations.length}
                      </span>
                    </div>
                  </div>
                )}

                <div className="action-row action-row-stacked">
                  <button className="button button-secondary back-action-button" onClick={() => { setShowOperationsPanel(false); setCurrentStep(1); }}>
                    <span className="action-icon"><ArrowLeftIcon /></span>
                    <span>Back to Form</span>
                  </button>
                  <button
                    className="button button-primary next-action-button"
                    onClick={toggleOperationsPanel}
                    disabled={runningOperations.length <= 1}
                  >
                    <span>Next operation</span>
                    <span className="action-icon"><ArrowRightIcon /></span>
                  </button>
                </div>

                <button
                  className="button button-ghost cancel-button"
                  onClick={handleTerminateOperation}
                >
                  <TrashIcon />
                  <span>Terminate Job</span>
                </button>
              </div>
            ) : (
              <>
                {currentStep === 1 && (
                  <div className="step-block">
                    <div
                      className={`upload-zone ${isDragOver ? 'drag-over' : ''}`}
                      onDragOver={handleDragOver}
                      onDragLeave={handleDragLeave}
                      onDrop={handleDrop}
                    >
                      <span className="upload-icon"><FolderIcon /></span>
                      <span className="upload-title">Drag & drop your CSV file</span>
                      <span className="upload-subtitle">or select a file from your device</span>
                      <label className="button button-primary select-file-button" style={{ display: 'inline-flex', alignItems: 'center', cursor: 'pointer' }}>
                        Select file
                        <input type="file" accept=".csv" style={{ display: 'none' }} onChange={(e) => e.target.files?.[0] && setCsvFile(e.target.files[0])} />
                      </label>
                    </div>

                    {csvFile && (
                      <div className="selected-file-card">
                        <div className="selected-file-main">
                          <span className="file-icon"><FileIcon /></span>
                          <span className="file-name">{csvFile.name}</span>
                        </div>
                        <button type="button" className="icon-button icon-button-ghost" disabled={isInspecting} onClick={() => setCsvFile(null)}>
                          <TrashIcon />
                        </button>
                      </div>
                    )}

                    <p className="helper-copy">Only .csv files are supported. Larger files may take longer to train.</p>

                    <div className="action-row">
                      <button className="button button-secondary inspect-button" disabled={!csvFile || isInspecting} onClick={handleInspectFile}>
                        <span className="action-icon"><GearIcon spinning={isInspecting} /></span>
                        <span>{isInspecting ? inspectStatusText : 'Inspect my file'}</span>
                      </button>
                      <button className="button button-primary next-action-button" disabled={csvColumns.length === 0 || isInspecting} onClick={() => setCurrentStep(2)}>
                        <span>Next</span>
                        <span className="action-icon"><ArrowRightIcon /></span>
                      </button>
                    </div>
                  </div>
                )}

                {currentStep === 2 && (
                  <div className="step-block">
                    <h3>Name your model</h3>
                    <label className="field-label">Model name</label>
                    <input type="text" placeholder="e.g. Weather_Predictor_Arena" value={modelName} onChange={(e) => setModelName(e.target.value)} />

                    <div className="sample-card-section">
                      <div className="sample-card-label">Sample card of your model</div>
                      <div className="model-preview-card">
                        <div className="model-preview-inner">
                          <div className="model-preview-icon-wrap">
                            <FolderIcon />
                          </div>
                          <div className="model-preview-meta">
                            <strong>{modelName || 'My model'}</strong>
                            <span>Sample size: 2.4 MB</span>
                          </div>
                        </div>
                        <div className="model-preview-footer">
                          <button className="icon-button icon-button-ghost" type="button"><DownloadIcon /></button>
                          <div className="menu-wrap">
                            <button className="icon-button icon-button-ghost" type="button" onClick={() => setSampleMenuOpen((value) => !value)}><MoreIcon /></button>
                            {sampleMenuOpen && (
                              <div className="menu-dropdown">
                                <button type="button" onClick={() => { setActiveModal('instructions'); setSampleMenuOpen(false); }}><span className="menu-icon"><FileIcon /></span>Instructions</button>
                                <button type="button" onClick={() => { setActiveModal('api-key'); setSampleMenuOpen(false); }}><span className="menu-icon"><KeyIcon /></span>API key</button>
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="action-row">
                      <button className="button button-secondary back-action-button" onClick={() => setCurrentStep(1)}>
                        <span className="action-icon"><ArrowLeftIcon /></span>
                        <span>Back</span>
                      </button>
                      <button className="button button-primary next-action-button" disabled={!modelName} onClick={() => setCurrentStep(3)}>
                        <span>Next</span>
                        <span className="action-icon"><ArrowRightIcon /></span>
                      </button>
                    </div>
                  </div>
                )}

                {currentStep === 3 && (
                  <div className="step-block">
                    <h3>Choose target columns</h3>
                    <label className="field-label">Target column</label>
                    <select value={selectedTarget} onChange={(e) => setSelectedTarget(e.target.value)}>
                      <option value="">Select target column</option>
                      {csvColumns.map((column) => (
                        <option key={column} value={column}>{column}</option>
                      ))}
                    </select>

                    <label className="field-label">Feature columns</label>
                    <div className="feature-list">
                      {csvColumns.filter((column) => column !== selectedTarget).map((column) => (
                        <label key={column} className="feature-item">
                          <input type="checkbox" checked={selectedFeatures.includes(column)} onChange={() => handleFeatureToggle(column)} />
                          <span>{column}</span>
                        </label>
                      ))}
                    </div>

                    <div className="action-row action-row-stacked">
                      <button className="button button-secondary back-action-button" onClick={() => setCurrentStep(2)}>
                        <span className="action-icon"><ArrowLeftIcon /></span>
                        <span>Back</span>
                      </button>
                      <button className="button button-primary next-action-button" disabled={!selectedTarget || selectedFeatures.length === 0 || isInspecting} onClick={handleGenerateModel}>
                        <span className="action-icon"><GearIcon spinning={isInspecting} /></span>
                        <span>{isInspecting ? inspectStatusText : 'Generate model'}</span>
                      </button>
                    </div>

                    <button
                      className="button button-ghost cancel-button"
                      onClick={handleTerminateOperation}
                    >
                      <TrashIcon />
                      <span>Terminate Job</span>
                    </button>
                  </div>
                )}
              </>
            )}
          </div>
        </div>

        <div className="panel-footer-fixed">
          <button className="button button-ghost lower-model-button" onClick={openModelsPanel}>
            <span className="action-icon"><FolderIcon /></span>
            <span>My models</span>
          </button>
        </div>
      </section>

      {/* COLUMN 2: REGISTRY & HOMEPAGE INTRO TEXT */}
      <section className="panel panel-right">
        <div className="dashboard-card">
          <div className="dashboard-topbar">
            <div className="topbar-left-wrapper">
              <button
                className="mobile-back-view-arrow"
                onClick={() => setMobileActiveColumn('first')}
                aria-label="Back to primary controls"
              >
                <ArrowLeftIcon />
              </button>
              <div>
                <h3>Welcome back</h3>
                <p>{userEmail || 'Your account is ready'}</p>
              </div>
            </div>
            <div className="dashboard-actions">
              <button className="icon-button" onClick={() => setProfileDropdown((value) => !value)}><UserIcon /></button>
              <button className="icon-button" onClick={handleLogout}><LogoutIcon /></button>
            </div>
          </div>

          {profileDropdown && (
            <div className="profile-card">
              <h4>User details</h4>
              <p><strong>Email:</strong> {userEmail}</p>
              <p><strong>ID:</strong> {userId}</p>
            </div>
          )}

          <div className="divider-fade" />

          {rightPanelContent === 'default' && (
            <div className="default-state">
              <div className="intro-text-wrapper">
                <h2>
                  Train your model today and get a{' '}
                  <span className="highlight-pill">custom model</span>
                </h2>
                <p>Create a production-ready deployment flow for your datasets with custom training and instant API access.</p>
              </div>
              <div className="copyright-at-bottom">© 2026 AutoML Engine</div>
            </div>
          )}

          {rightPanelContent === 'models' && (
            <div className="models-panel">
              <div className="models-panel-header">
                <h3>My files</h3>
                <div className="search-shell">
                  <SearchIcon />
                  <input
                    type="text"
                    value={searchQuery}
                    placeholder="Search my models"
                    onChange={(e) => setSearchQuery(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && setAppliedSearch(searchQuery)}
                  />
                  <button type="button" className="icon-button icon-button-ghost" onClick={() => setAppliedSearch(searchQuery)}><ArrowRightIcon /></button>
                </div>
              </div>

              <div className="models-list-scrollable">
                {visibleModels.length === 0 ? (
                  <div className="empty-models">
                    <div className="empty-icon"><FolderIcon /></div>
                    <p>No models in your account yet.</p>
                  </div>
                ) : (
                  <div className="model-grid">
                    {visibleModels.map((model) => (
                      <div key={model.id} className="model-preview-card actual-model-card">
                        <div className="model-preview-inner">
                          <div className="model-preview-icon-wrap">
                            <FolderIcon />
                          </div>
                          <div className="model-preview-meta">
                            <strong>{model.model_name?.toUpperCase() || 'MODEL'}</strong>
                            <span>{model.model_size || '2.4 MB'}</span>
                          </div>
                        </div>
                        <div className="model-preview-footer">
                          <a className="icon-button icon-button-ghost" href={`/developer/models/download/${model.id}`}><DownloadIcon /></a>
                          <div className="menu-wrap">
                            <button className="icon-button icon-button-ghost" onClick={() => setDetailsMenuOpen((current) => current === model.id ? null : model.id)}><MoreIcon /></button>
                            {detailsMenuOpen === model.id && (
                              <div className="menu-dropdown">
                                <button type="button" onClick={() => { setSelectedModel(model); setActiveModal('predict'); setDetailsMenuOpen(null); }}><span className="menu-icon"><GearIcon /></span>Predict Data</button>
                                <button type="button" onClick={() => { setSelectedModel(model); setActiveModal('instructions'); setDetailsMenuOpen(null); }}><span className="menu-icon"><FileIcon /></span>Instructions</button>
                                <button type="button" onClick={() => { setSelectedModel(model); setActiveModal('api-key'); setDetailsMenuOpen(null); }}><span className="menu-icon"><KeyIcon /></span>API key</button>
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </section>

      {activeModal && (
        <div className="modal-overlay" onClick={() => setActiveModal(null)}>
          <div className="modal-card" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" type="button" onClick={() => setActiveModal(null)}><CloseIcon /></button>
            
            {activeModal === 'predict' && (
              <div className="predict-modal-content">
                <h3>Predict Data</h3>
                <p className="predict-subtitle">
                  Model: <strong>{selectedModel?.model_name || 'Unnamed Engine'}</strong> (v{selectedModel?.model_version || 1})
                </p>
                <div className="divider-fade" style={{ margin: '1rem 0' }} />
                
                <form onSubmit={handleExecutePrediction} className="auth-form predict-dynamic-form">
                  <div className="scrollable-features-inputs" style={{ maxHeight: '40vh', overflowY: 'auto', paddingRight: '4px' }}>
                    {currentModelFeatures.length === 0 ? (
                      <p className="helper-text">No custom feature columns detected for this machine learning model package.</p>
                    ) : (
                      currentModelFeatures.map((feature) => (
                        <div key={feature} className="predict-input-field-group" style={{ marginBottom: '1rem', display: 'flex', flexDirection: 'column' }}>
                          <label className="field-label" style={{ marginBottom: '4px', textAlign: 'left', fontWeight: '500' }}>{feature}</label>
                          <input
                            type="text"
                            placeholder={`Enter values for ${feature}`}
                            value={predictInputs[feature] || ''}
                            onChange={(e) => handlePredictInputValueChange(feature, e.target.value)}
                            required
                          />
                        </div>
                      ))
                    )}
                  </div>

                  <div className="divider-fade" style={{ margin: '1rem 0' }} />

                  <button 
                    type="submit" 
                    className="button button-primary" 
                    disabled={isPredictingLoading || currentModelFeatures.length === 0}
                  >
                    {isPredictingLoading ? 'Calculating Inference...' : 'Predict my data'}
                  </button>
                </form>

                {predictionResult && (
                  <div className="prediction-result-display-matrix" style={{ marginTop: '1.5rem', padding: '1rem', borderRadius: '6px', background: predictionResult.success ? '#eff6ff' : '#fef2f2', border: predictionResult.success ? '1px solid #bfdbfe' : '1px solid #fca5a5' }}>
                    {predictionResult.success ? (
                      <div>
                        <span style={{ fontSize: '0.85rem', color: '#1e40af', fontWeight: '600', display: 'block', marginBottom: '4px' }}>PREDICTION SUCCESSFUL</span>
                        <strong style={{ fontSize: '1.5rem', color: '#1d4ed8' }}>{predictionResult.value}</strong>
                      </div>
                    ) : (
                      <div>
                        <span style={{ fontSize: '0.85rem', color: '#991b1b', fontWeight: '600', display: 'block', marginBottom: '4px' }}>EXECUTION FAULT</span>
                        <p style={{ margin: 0, fontSize: '0.9rem', color: '#b91c1c' }}>{predictionResult.error}</p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}

            {activeModal === 'instructions' && (
              <div>
                <h3>Instructions</h3>
                <p>Step 1: Connect to the prediction endpoint using your bearer token.</p>
                <div className="code-block">
                  <pre>{`curl -X POST "/v1/predict" \\
-H "Authorization: Bearer ${selectedModel?.api_key || 'YOUR_TOKEN'}" \\
-H "Content-Type: application/json" \\
-d '{"feature_1": 0.1, "feature_2": 0.2}'`}</pre>
                  <button className="icon-button icon-button-ghost" type="button" onClick={() => handleCopyText(`curl -X POST "/v1/predict" ...`, 'instructions')}>
                    {isCopying.instructions ? 'Copied!' : <CopyIcon />}
                  </button>
                </div>
                <p>Step 2: Send your feature payload and receive the prediction response.</p>
              </div>
            )}

            {activeModal === 'api-key' && (
              <div>
                <h3>Secrets</h3>
                <p>API key</p>
                <div className="secret-card">
                  <span>{selectedModel?.api_key || 'No API key available'}</span>
                  <button className="icon-button icon-button-ghost" type="button" onClick={() => handleCopyText(selectedModel?.api_key || '', 'key')}>
                    {isCopying.key ? 'Copied!' : <CopyIcon />}
                  </button>
                </div>
                <p>API URL</p>
                <div className="secret-card">
                  <span>{`/v1/predict`}</span>
                  <button className="icon-button icon-button-ghost" type="button" onClick={() => handleCopyText(`/v1/predict`, 'url')}>
                    {isCopying.url ? 'Copied!' : <CopyIcon />}
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}