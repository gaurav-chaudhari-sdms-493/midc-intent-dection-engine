import React, { useState, useEffect, useMemo } from 'react';
import styles from './TaxonomyManager.module.css';
import { Edit, Trash2, Plus, Check, X } from 'lucide-react';

// --- Mock Data Generation ---
const initialIntents = [
  {
    id: 'intent-1',
    name: 'New Investment Proposal',
    keywords: ['investment', 'proposal', 'new project', 'funding', 'capital', 'startup']
  },
  {
    id: 'intent-2',
    name: 'Land/Plot Allotment',
    keywords: ['land', 'plot', 'area', 'allotment', 'industrial zone', 'MIDC land', 'lease']
  },
  {
    id: 'intent-3',
    name: 'Policy/Incentive Query',
    keywords: ['policy', 'guideline', 'rule', 'regulation', 'clarification', 'incentive', 'subsidy', 'scheme']
  },
  {
    id: 'intent-4',
    name: 'Application Status',
    keywords: ['application', 'status', 'update', 'tracking', 'progress', 'submitted']
  },
  {
    id: 'intent-5',
    name: 'Complaint/Grievance',
    keywords: ['complaint', 'grievance', 'issue', 'problem', 'feedback', 'escalation']
  },
  {
    id: 'intent-6',
    name: 'General FAQ',
    keywords: ['general', 'query', 'information', 'ask', 'faq', 'common questions']
  },
];

const TaxonomyManager = () => {
  const [intents, setIntents] = useState(initialIntents);
  const [originalIntents, setOriginalIntents] = useState(initialIntents); // To track changes
  const [selectedIntentId, setSelectedIntentId] = useState(intents[0]?.id || null);
  const [editingIntentNameId, setEditingIntentNameId] = useState(null);
  const [editingIntentNameValue, setEditingIntentNameValue] = useState('');
  const [newKeywordInput, setNewKeywordInput] = useState('');

  const hasChanges = useMemo(() => {
    return JSON.stringify(intents) !== JSON.stringify(originalIntents);
  }, [intents, originalIntents]);

  const selectedIntent = useMemo(() => {
    return intents.find(intent => intent.id === selectedIntentId);
  }, [intents, selectedIntentId]);

  // --- Intent Name Editing ---
  const handleEditIntentName = (intentId, currentName) => {
    setEditingIntentNameId(intentId);
    setEditingIntentNameValue(currentName);
  };

  const handleSaveIntentName = (intentId) => {
    if (editingIntentNameValue.trim() === '') {
      alert("Intent name cannot be empty.");
      return;
    }
    setIntents(prevIntents =>
      prevIntents.map(intent =>
        intent.id === intentId ? { ...intent, name: editingIntentNameValue.trim() } : intent
      )
    );
    setEditingIntentNameId(null);
    setEditingIntentNameValue('');
  };

  const handleCancelEditIntentName = () => {
    setEditingIntentNameId(null);
    setEditingIntentNameValue('');
  };

  // --- Intent Management ---
  const handleDeleteIntent = (intentId) => {
    if (window.confirm("Are you sure you want to delete this intent? This action cannot be undone.")) {
      setIntents(prevIntents => prevIntents.filter(intent => intent.id !== intentId));
      if (selectedIntentId === intentId) {
        setSelectedIntentId(null); // Deselect if deleted
      }
    }
  };

  const handleAddNewIntent = () => {
    const newId = `intent-${Date.now()}`; // Unique ID
    const newIntent = { id: newId, name: `New Intent ${intents.length + 1}`, keywords: [] };
    setIntents(prevIntents => [...prevIntents, newIntent]);
    setSelectedIntentId(newId); // Select the newly added intent
    handleEditIntentName(newId, newIntent.name); // Immediately go into edit mode
  };

  // --- Keyword Management ---
  const handleAddKeyword = () => {
    if (!selectedIntent) return;
    const keyword = newKeywordInput.trim().toLowerCase();
    if (keyword && !selectedIntent.keywords.includes(keyword)) {
      setIntents(prevIntents =>
        prevIntents.map(intent =>
          intent.id === selectedIntentId
            ? { ...intent, keywords: [...intent.keywords, keyword] }
            : intent
        )
      );
      setNewKeywordInput('');
    }
  };

  const handleDeleteKeyword = (keywordToDelete) => {
    if (!selectedIntent) return;
    setIntents(prevIntents =>
      prevIntents.map(intent =>
        intent.id === selectedIntentId
          ? { ...intent, keywords: intent.keywords.filter(keyword => keyword !== keywordToDelete) }
          : intent
      )
    );
  };

  // --- Save/Discard Changes ---
  const handleSaveChanges = () => {
    // In a real application, this would send the 'intents' state to a backend API
    console.log("Saving changes:", intents);
    setOriginalIntents(intents); // Update original to reflect saved state
    alert("Changes saved successfully! (Mock save)");
  };

  const handleDiscardChanges = () => {
    if (window.confirm("Are you sure you want to discard all unsaved changes?")) {
      setIntents(originalIntents); // Revert to original state
      setSelectedIntentId(originalIntents[0]?.id || null); // Reset selection
      setEditingIntentNameId(null);
      setEditingIntentNameValue('');
      setNewKeywordInput('');
    }
  };

  return (
    <div className={styles.taxonomyManager}>
      <div className={styles.warningBanner}>
        Changes here affect live classification — coordinate with the ML team before publishing.
      </div>

      <div className={styles.contentArea}>
        {/* Left Column: Primary Intents */}
        <div className={styles.primaryIntentsColumn}>
          <h3>Primary Intents</h3>
          {intents.map(intent => (
            <div
              key={intent.id}
              className={`${styles.intentListItem} ${selectedIntentId === intent.id ? styles.selected : ''}`}
              onClick={() => setSelectedIntentId(intent.id)}
            >
              {editingIntentNameId === intent.id ? (
                <input
                  type="text"
                  className={styles.intentNameInput}
                  value={editingIntentNameValue}
                  onChange={(e) => setEditingIntentNameValue(e.target.value)}
                  onKeyPress={(e) => { if (e.key === 'Enter') handleSaveIntentName(intent.id); }}
                  onBlur={() => handleSaveIntentName(intent.id)} // Save on blur
                  autoFocus
                />
              ) : (
                <>
                  <span>{intent.name}</span>
                  <button onClick={(e) => { e.stopPropagation(); handleEditIntentName(intent.id, intent.name); }} title="Edit Intent Name">
                    <Edit size={18} />
                  </button>
                  <button onClick={(e) => { e.stopPropagation(); handleDeleteIntent(intent.id); }} title="Delete Intent">
                    <Trash2 size={18} />
                  </button>
                </>
              )}
            </div>
          ))}
          <button onClick={handleAddNewIntent} className={styles.addIntentButton}>
            <Plus size={18} style={{ marginRight: '8px' }} /> Add New Intent
          </button>
        </div>

        {/* Right Column: Keywords/Example Phrases */}
        <div className={styles.keywordsColumn}>
          {selectedIntent ? (
            <>
              <h3>Keywords for "{selectedIntent.name}"</h3>
              <div className={styles.keywordList}>
                {selectedIntent.keywords.map((keyword, index) => (
                  <span key={index} className={styles.keywordItem}>
                    {keyword}
                    <button onClick={() => handleDeleteKeyword(keyword)} title="Remove Keyword">
                      <X size={14} />
                    </button>
                  </span>
                ))}
              </div>
              <div className={styles.keywordInputGroup}>
                <input
                  type="text"
                  className={styles.keywordInput}
                  placeholder="Add new keyword"
                  value={newKeywordInput}
                  onChange={(e) => setNewKeywordInput(e.target.value)}
                  onKeyPress={(e) => { if (e.key === 'Enter') handleAddKeyword(); }}
                />
                <button onClick={handleAddKeyword} className={styles.addKeywordButton}>
                  <Plus size={18} /> Add
                </button>
              </div>
            </>
          ) : (
            <div className={styles.noIntentSelected}>
              <p>Select an intent from the left to manage its keywords.</p>
            </div>
          )}
        </div>
      </div>

      {/* Action Buttons at bottom */}
      <div className={styles.actionButtonsContainer}>
        <button
          onClick={handleDiscardChanges}
          className={`${styles.actionButton} ${styles.discard}`}
          disabled={!hasChanges}
        >
          Discard
        </button>
        <button
          onClick={handleSaveChanges}
          className={`${styles.actionButton} ${styles.save}`}
          disabled={!hasChanges}
        >
          Save Changes
        </button>
      </div>
    </div>
  );
};

export default TaxonomyManager;
