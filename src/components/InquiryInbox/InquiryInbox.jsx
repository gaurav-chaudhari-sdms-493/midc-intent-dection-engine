import React, { useState, useMemo } from 'react';
import styles from './InquiryInbox.module.css';
import { mockInquiries } from '../../data/mockInquiries'; // Import mock inquiries

// --- Helper Functions ---
const formatRelativeTime = (dateString) => {
  const date = new Date(dateString);
  const now = new Date();
  const seconds = Math.round((now.getTime() - date.getTime()) / 1000);
  const minutes = Math.round(seconds / 60);
  const hours = Math.round(minutes / 60);
  const days = Math.round(hours / 24);

  if (seconds < 60) return `${seconds}s ago`;
  if (minutes < 60) return `${minutes}m ago`;
  if (hours < 24) return `${hours}h ago`;
  if (days < 7) return `${days}d ago`;
  return date.toLocaleDateString(); // Fallback for older dates
};

const getPriorityStripeClass = (priority) => {
  switch (priority) {
    case 'High': return styles.priorityHigh;
    case 'Medium': return styles.priorityMedium;
    case 'Low': return styles.priorityLow;
    case 'Informational': return styles.priorityInformational;
    default: return '';
  }
};

const truncateText = (text, maxLength) => {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

const InquiryInbox = ({ onInquirySelect }) => {
  const [industryFilter, setIndustryFilter] = useState('');
  const [intentFilter, setIntentFilter] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('');
  const [languageFilter, setLanguageFilter] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  // Derive filter options from mock data
  const availableIndustries = useMemo(() => {
    const unique = new Set(mockInquiries.map(i => i.industry));
    return Array.from(unique).sort();
  }, []);

  const availableIntents = useMemo(() => {
    const unique = new Set(mockInquiries.map(i => i.primary_intent));
    return Array.from(unique).sort();
  }, []);

  const availableLanguages = useMemo(() => {
    const unique = new Set(mockInquiries.map(i => i.original_language));
    return Array.from(unique).sort();
  }, []);

  const availablePriorities = useMemo(() => {
    const unique = new Set(mockInquiries.map(i => i.priority));
    // Order priorities specifically
    const order = { 'High': 1, 'Medium': 2, 'Low': 3, 'Informational': 4 };
    return Array.from(unique).sort((a, b) => order[a] - order[b]);
  }, []);

  const filteredInquiries = useMemo(() => {
    return mockInquiries.filter(inquiry => {
      let matches = true;

      if (industryFilter && inquiry.industry !== industryFilter) {
        matches = false;
      }
      if (intentFilter && inquiry.primary_intent !== intentFilter) {
        matches = false;
      }
      if (priorityFilter && inquiry.priority !== priorityFilter) {
        matches = false;
      }
      if (languageFilter && inquiry.original_language !== languageFilter.toLowerCase()) {
        matches = false;
      }
      if (searchTerm) {
        const lowerSearchTerm = searchTerm.toLowerCase();
        const inquiryText = inquiry.original_text || '';
        const investorName = inquiry.investor_name || '';

        if (
          !investorName.toLowerCase().includes(lowerSearchTerm) &&
          !inquiryText.toLowerCase().includes(lowerSearchTerm) &&
          !inquiry.industry.toLowerCase().includes(lowerSearchTerm) &&
          !inquiry.primary_intent.toLowerCase().includes(lowerSearchTerm)
        ) {
          matches = false;
        }
      }
      return matches;
    });
  }, [industryFilter, intentFilter, priorityFilter, languageFilter, searchTerm]);

  return (
    <div className={styles.inquiryInbox}>
      <div className={styles.filterBar}>
        <div className={styles.filterGroup}>
          <label htmlFor="industry">Industry:</label>
          <select id="industry" value={industryFilter} onChange={(e) => setIndustryFilter(e.target.value)}>
            <option value="">All</option>
            {availableIndustries.map(ind => <option key={ind} value={ind}>{ind}</option>)}
          </select>
        </div>

        <div className={styles.filterGroup}>
          <label htmlFor="intent">Intent:</label>
          <select id="intent" value={intentFilter} onChange={(e) => setIntentFilter(e.target.value)}>
            <option value="">All</option>
            {availableIntents.map(int => <option key={int} value={int}>{int}</option>)}
          </select>
        </div>

        <div className={styles.filterGroup}>
          <label htmlFor="priority">Priority:</label>
          <select id="priority" value={priorityFilter} onChange={(e) => setPriorityFilter(e.target.value)}>
            <option value="">All</option>
            {availablePriorities.map(p => <option key={p} value={p}>{p}</option>)}
          </select>
        </div>

        <div className={styles.filterGroup}>
          <label htmlFor="language">Language:</label>
          <select id="language" value={languageFilter} onChange={(e) => setLanguageFilter(e.target.value)}>
            <option value="">All</option>
            {availableLanguages.map(lang => <option key={lang} value={lang.toUpperCase()}>{lang.toUpperCase()}</option>)}
          </select>
        </div>

        <input
          type="search"
          placeholder="Search inquiries..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />

        {(industryFilter || intentFilter || priorityFilter || languageFilter || searchTerm) && (
          <button className={styles.clearFiltersButton} onClick={handleClearFilters}>
            Clear Filters
          </button>
        )}
      </div>

      {filteredInquiries.length > 0 ? (
        <div className={styles.inquiryList}>
          {filteredInquiries.map(inquiry => {
            const slaDeadline = inquiry.sla_deadline ? new Date(inquiry.sla_deadline) : null;
            const now = new Date();
            const slaRemainingMs = slaDeadline ? slaDeadline.getTime() - now.getTime() : null;
            const showSlaCountdown = slaRemainingMs !== null && slaRemainingMs > 0 && slaRemainingMs < (2 * 60 * 60 * 1000); // < 2 hours

            return (
              <div
                key={inquiry.inquiry_id}
                className={styles.inquiryCard}
                onClick={() => onInquirySelect(inquiry.inquiry_id)}
              >
                <div className={`${styles.priorityStripe} ${getPriorityStripeClass(inquiry.priority)}`} />
                <div className={styles.cardHeader}>
                  <span className={styles.senderName}>{inquiry.investor_name || "Anonymous"}</span>
                  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end' }}>
                    <span className={styles.timestamp}>{formatRelativeTime(inquiry.created_at)}</span>
                    {showSlaCountdown && (
                      <span className={styles.slaCountdown}>
                        SLA: {Math.ceil(slaRemainingMs / (60 * 1000))}m left
                      </span>
                    )}
                  </div>
                </div>
                <p className={styles.inquiryPreview}>{truncateText(inquiry.original_text || '', 120)}</p>
                <div className={styles.cardFooter}>
                  <span className={`${styles.tag} ${styles.industryTag}`}>{inquiry.industry}</span>
                  <span className={`${styles.tag} ${styles.intentTag}`}>{inquiry.primary_intent}</span>
                  <span className={`${styles.tag} ${styles.languageBadge}`}>{inquiry.original_language.toUpperCase()}</span>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className={styles.emptyState}>
          <p>No inquiries match these filters.</p>
          <button onClick={handleClearFilters}>Clear Filters</button>
        </div>
      )}
    </div>
  );
};

export default InquiryInbox;
