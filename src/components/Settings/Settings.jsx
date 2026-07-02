import React, { useState, useMemo } from 'react';
import styles from './Settings.module.css';

const Settings = () => {
  // Mock state for various settings
  const [apiKeys, setApiKeys] = useState({
    bhashini: '********************', // Placeholder for masked key
    anthropic: '********************',
  });
  const [imapSettings, setImapSettings] = useState({
    host: 'imap.example.com',
    user: 'officer@midc.gov.in',
    password: '********************',
  });
  const [thresholds, setThresholds] = useState({
    confidence: 75, // Percentage
    slaWarning: 120, // Minutes
  });
  const [notificationPreferences, setNotificationPreferences] = useState({
    email: true,
    sms: false,
    inApp: true,
  });

  // State to track changes
  const [originalApiKeys] = useState(apiKeys);
  const [originalImapSettings] = useState(imapSettings);
  const [originalThresholds] = useState(thresholds);
  const [originalNotificationPreferences] = useState(notificationPreferences);

  const hasChanges = useMemo(() => {
    return (
      JSON.stringify(apiKeys) !== JSON.stringify(originalApiKeys) ||
      JSON.stringify(imapSettings) !== JSON.stringify(originalImapSettings) ||
      JSON.stringify(thresholds) !== JSON.stringify(originalThresholds) ||
      JSON.stringify(notificationPreferences) !== JSON.stringify(originalNotificationPreferences)
    );
  }, [apiKeys, originalApiKeys, imapSettings, originalImapSettings, thresholds, originalThresholds, notificationPreferences, originalNotificationPreferences]);

  const handleApiKeyChange = (key, value) => {
    setApiKeys(prev => ({ ...prev, [key]: value }));
  };

  const handleImapSettingChange = (key, value) => {
    setImapSettings(prev => ({ ...prev, [key]: value }));
  };

  const handleThresholdChange = (key, value) => {
    setThresholds(prev => ({ ...prev, [key]: Number(value) }));
  };

  const handleNotificationChange = (key, value) => {
    setNotificationPreferences(prev => ({ ...prev, [key]: value }));
  };

  const handleSaveChanges = () => {
    // In a real app, send these settings to a backend API
    console.log("Saving settings:", { apiKeys, imapSettings, thresholds, notificationPreferences });
    alert("Settings saved successfully! (Mock save)");
    // Update original states to reflect saved changes
    setApiKeys(apiKeys);
    setImapSettings(imapSettings);
    setThresholds(thresholds);
    setNotificationPreferences(notificationPreferences);
  };

  const handleDiscardChanges = () => {
    if (window.confirm("Are you sure you want to discard all unsaved changes?")) {
      setApiKeys(originalApiKeys);
      setImapSettings(originalImapSettings);
      setThresholds(originalThresholds);
      setNotificationPreferences(originalNotificationPreferences);
    }
  };

  // Mock connection test state
  const [imapTestResult, setImapTestResult] = useState(null); // null, 'success', 'error'

  const handleTestImapConnection = () => {
    setImapTestResult(null);
    // Simulate API call
    setTimeout(() => {
      if (Math.random() > 0.3) { // 70% chance of success
        setImapTestResult('success');
      } else {
        setImapTestResult('error');
      }
    }, 1000);
  };

  return (
    <div className={styles.settings}>
      <h2>Application Settings</h2>

      {/* API Keys Section */}
      <div className={styles.section}>
        <h3 className={styles.sectionTitle}>API Integrations</h3>
        <div className={styles.formGroup}>
          <label htmlFor="bhashiniApiKey">Bhashini API Key</label>
          <input
            type="password"
            id="bhashiniApiKey"
            value={apiKeys.bhashini}
            onChange={(e) => handleApiKeyChange('bhashini', e.target.value)}
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="anthropicApiKey">Anthropic API Key</label>
          <input
            type="password"
            id="anthropicApiKey"
            value={apiKeys.anthropic}
            onChange={(e) => handleApiKeyChange('anthropic', e.target.value)}
          />
        </div>
      </div>

      {/* IMAP Settings Section */}
      <div className={styles.section}>
        <h3 className={styles.sectionTitle}>Email Ingestion (IMAP)</h3>
        <div className={styles.formGroup}>
          <label htmlFor="imapHost">IMAP Host</label>
          <input
            type="text"
            id="imapHost"
            value={imapSettings.host}
            onChange={(e) => handleImapSettingChange('host', e.target.value)}
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="imapUser">IMAP Username</label>
          <input
            type="text"
            id="imapUser"
            value={imapSettings.user}
            onChange={(e) => handleImapSettingChange('user', e.target.value)}
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="imapPassword">IMAP Password</label>
          <input
            type="password"
            id="imapPassword"
            value={imapSettings.password}
            onChange={(e) => handleImapSettingChange('password', e.target.value)}
          />
        </div>
        <button onClick={handleTestImapConnection} className={styles.testConnectionButton}>
          Test Connection
        </button>
        {imapTestResult === 'success' && (
          <span className={`${styles.testConnectionResult} ${styles.success}`}>Connection successful!</span>
        )}
        {imapTestResult === 'error' && (
          <span className={`${styles.testConnectionResult} ${styles.error}`}>Connection failed. Check credentials.</span>
        )}
      </div>

      {/* Thresholds Section */}
      <div className={styles.section}>
        <h3 className={styles.sectionTitle}>System Thresholds</h3>
        <div className={styles.formGroup}>
          <label htmlFor="confidenceThreshold">Classification Confidence Threshold: {thresholds.confidence}%</label>
          <input
            type="range"
            id="confidenceThreshold"
            min="0"
            max="100"
            step="5"
            value={thresholds.confidence}
            onChange={(e) => handleThresholdChange('confidence', e.target.value)}
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="slaWarningThreshold">SLA Warning Threshold: {thresholds.slaWarning} minutes</label>
          <input
            type="range"
            id="slaWarningThreshold"
            min="30"
            max="240"
            step="15"
            value={thresholds.slaWarning}
            onChange={(e) => handleThresholdChange('slaWarning', e.target.value)}
          />
        </div>
      </div>

      {/* Notification Preferences Section */}
      <div className={styles.section}>
        <h3 className={styles.sectionTitle}>Notification Preferences</h3>
        <div className={styles.formGroup}>
          <label>
            <input
              type="checkbox"
              checked={notificationPreferences.email}
              onChange={(e) => handleNotificationChange('email', e.target.checked)}
            /> Email Notifications
          </label>
        </div>
        <div className={styles.formGroup}>
          <label>
            <input
              type="checkbox"
              checked={notificationPreferences.sms}
              onChange={(e) => handleNotificationChange('sms', e.target.checked)}
            /> SMS Notifications
          </label>
        </div>
        <div className={styles.formGroup}>
          <label>
            <input
              type="checkbox"
              checked={notificationPreferences.inApp}
              onChange={(e) => handleNotificationChange('inApp', e.target.checked)}
            /> In-App Notifications
          </label>
        </div>
      </div>

      {/* User Management (Placeholder) */}
      <div className={styles.section}>
        <h3 className={styles.sectionTitle}>User Management</h3>
        <p className={styles.userManagementPlaceholder}>
          User roles and permissions management will be implemented here.
        </p>
      </div>

      {/* Action Buttons */}
      <div className={styles.buttonGroup}>
        <button
          onClick={handleDiscardChanges}
          className={`${styles.actionButton} ${styles.secondary}`}
          disabled={!hasChanges}
        >
          Discard Changes
        </button>
        <button
          onClick={handleSaveChanges}
          className={`${styles.actionButton} ${styles.primary}`}
          disabled={!hasChanges}
        >
          Save Changes
        </button>
      </div>
    </div>
  );
};

export default Settings;
