import React, { useState, useMemo } from 'react';
import styles from './RoutingQueue.module.css';
import { mockInquiries } from '../../data/mockInquiries'; // Import mock inquiries

const routingStatuses = ["New", "In Review", "Escalated", "Resolved"];

// --- Helper Functions (re-using from InquiryInbox) ---
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
  return date.toLocaleDateString();
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

const RoutingQueue = ({ onInquirySelect }) => {
  // Initialize state with mockInquiries, ensuring routing_status is present
  const [inquiries, setInquiries] = useState(mockInquiries.map(inq => ({
    ...inq,
    routing_status: inq.routing_status || 'New' // Ensure a default status if missing
  })));

  const inquiriesByStatus = useMemo(() => {
    const grouped = {};
    routingStatuses.forEach(status => {
      grouped[status] = inquiries.filter(inq => inq.routing_status === status);
    });
    return grouped;
  }, [inquiries]);

  const handleMoveInquiry = (inquiryId, newStatus) => {
    setInquiries(prevInquiries =>
      prevInquiries.map(inquiry =>
        inquiry.inquiry_id === inquiryId ? { ...inquiry, routing_status: newStatus } : inquiry
      )
    );
  };

  const getColumnClass = (status) => {
    switch (status) {
      case 'New': return styles.new;
      case 'In Review': return styles.inReview;
      case 'Escalated': return styles.escalated;
      case 'Resolved': return styles.resolved;
      default: return '';
    }
  };

  return (
    <div className={styles.routingQueue}>
      <div className={styles.kanbanBoard}>
        {routingStatuses.map(status => (
          <div key={status} className={`${styles.column} ${getColumnClass(status)}`}>
            <div className={styles.columnHeader}>
              <h3 className={styles.columnTitle}>{status}</h3>
              <span className={styles.countBadge}>{inquiriesByStatus[status].length}</span>
            </div>
            <div className={styles.columnContent}>
              {inquiriesByStatus[status].length > 0 ? (
                inquiriesByStatus[status].map(inquiry => {
                  const slaDeadline = inquiry.sla_deadline ? new Date(inquiry.sla_deadline) : null;
                  const now = new Date();
                  const slaRemainingMs = slaDeadline ? slaDeadline.getTime() - now.getTime() : null;
                  const showSlaCountdown = slaRemainingMs !== null && slaRemainingMs > 0 && inquiry.priority === 'Medium' && slaRemainingMs < (2 * 60 * 60 * 1000); // < 2 hours for Medium priority

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
                      <p className={styles.inquiryPreview}>{truncateText(inquiry.original_text || '', 80)}</p>
                      <div className={styles.cardFooter}>
                        <select
                          className={styles.moveDropdown}
                          value={inquiry.routing_status}
                          onChange={(e) => handleMoveInquiry(inquiry.inquiry_id, e.target.value)}
                          onClick={(e) => e.stopPropagation()} // Prevent card click when opening dropdown
                        >
                          <option value="">Move to...</option>
                          {routingStatuses.map(s => (
                            <option key={s} value={s} disabled={s === inquiry.routing_status}>
                              {s}
                            </option>
                          ))}
                        </select>
                      </div>
                    </div>
                  );
                })
              ) : (
                <div className={styles.emptyColumn}>No inquiries in this status.</div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RoutingQueue;
