import React, { useState, useEffect } from 'react';
import styles from './InquiryDetail.module.css';
import { X } from 'lucide-react';

// --- Extended Mock Data Generation (similar to InquiryInbox but with more detail) ---
const industries = [
  "IT & Software", "Automotive", "Pharmaceuticals", "Chemicals", "Textiles",
  "Food Processing", "Electronics", "Infrastructure", "Renewable Energy", "Logistics"
];
const intents = [
  "New Investment Proposal", "Land Allocation Inquiry", "Policy Clarification",
  "Infrastructure Request", "Partnership Opportunity", "SLA Extension Request",
  "General Inquiry", "Expansion Plan"
];
const languages = ["en", "hi", "mr"];
const priorities = ["High", "Medium", "Low", "Informational"];
const locations = ["Pune", "Nagpur", "Mumbai", "Aurangabad", "Nashik", "Thane"];
const assignedTo = ["Officer A. Sharma", "Officer B. Singh", "Officer C. Patel", "Auto-resolved"];

const generateDetailedInquiry = (id) => {
  const sender = Math.random() > 0.2 ? `Investor ${String.fromCharCode(65 + Math.floor(Math.random() * 26))}. ${Math.floor(Math.random() * 100)}` : "Anonymous";
  const industry = industries[Math.floor(Math.random() * industries.length)];
  const intent = intents[Math.floor(Math.random() * intents.length)];
  const language = languages[Math.floor(Math.random() * languages.length)];
  const priority = priorities[Math.floor(Math.random() * priorities.length)];
  const location = locations[Math.floor(Math.random() * locations.length)];
  const assigned = assignedTo[Math.floor(Math.random() * assignedTo.length)];

  const originalTexts = {
    en: `Dear MIDC Team,

I am writing to express my strong interest in establishing a new manufacturing unit for ${industry} in the ${location} region. Our company, Global Innovations Inc., is a leader in sustainable technology and we believe Maharashtra offers an ideal environment for our expansion.

Could you please provide detailed information on available land parcels suitable for a 5-acre facility, along with any investment incentives or subsidies applicable to the ${industry} sector? We are particularly interested in understanding the process for environmental clearances and utility connections.

We anticipate an investment of approximately $${(Math.random() * 50 + 10).toFixed(2)} million and expect to generate around 200 local jobs. We look forward to your prompt response and guidance.

Sincerely,
${sender}`,
    hi: `प्रिय एमआईडीसी टीम,

मैं ${industry} के लिए ${location} क्षेत्र में एक नई विनिर्माण इकाई स्थापित करने में अपनी गहरी रुचि व्यक्त करने के लिए लिख रहा हूँ। हमारी कंपनी, ग्लोबल इनोवेशन इंक, सतत प्रौद्योगिकी में अग्रणी है और हम मानते हैं कि महाराष्ट्र हमारे विस्तार के लिए एक आदर्श वातावरण प्रदान करता है।

क्या आप 5 एकड़ की सुविधा के लिए उपयुक्त उपलब्ध भूमि पार्सल के बारे में विस्तृत जानकारी प्रदान कर सकते हैं, साथ ही ${industry} क्षेत्र पर लागू होने वाले किसी भी निवेश प्रोत्साहन या सब्सिडी के बारे में भी? हम विशेष रूप से पर्यावरणीय मंजूरी और उपयोगिता कनेक्शन की प्रक्रिया को समझने में रुचि रखते हैं।

हम लगभग $${(Math.random() * 50 + 10).toFixed(2)} मिलियन के निवेश की उम्मीद करते हैं और लगभग 200 स्थानीय रोजगार पैदा करने की उम्मीद करते हैं। हम आपके शीघ्र जवाब और मार्गदर्शन की प्रतीक्षा कर रहे हैं।

साभार,
${sender}`,
    mr: `प्रिय एमआयडीसी टीम,

मी ${industry} साठी ${location} प्रदेशात नवीन उत्पादन युनिट स्थापन करण्यामध्ये माझी तीव्र स्वारस्य व्यक्त करण्यासाठी लिहित आहे. आमची कंपनी, ग्लोबल इनोव्हेशन्स इंक, शाश्वत तंत्रज्ञानामध्ये आघाडीवर आहे आणि आम्हाला विश्वास आहे की महाराष्ट्र आमच्या विस्तारासाठी एक आदर्श वातावरण प्रदान करते.

तुम्ही 5 एकर सुविधेसाठी योग्य असलेल्या उपलब्ध भूखंडांची सविस्तर माहिती देऊ शकता का, तसेच ${industry} क्षेत्राला लागू होणाऱ्या कोणत्याही गुंतवणूक प्रोत्साहन किंवा सबसिडीबद्दल? आम्हाला विशेषतः पर्यावरणीय मंजुरी आणि उपयुक्तता जोडणीची प्रक्रिया समजून घेण्यास स्वारस्य आहे.

आम्ही अंदाजे $${(Math.random() * 50 + 10).toFixed(2)} दशलक्ष गुंतवणुकीची अपेक्षा करतो आणि सुमारे 200 स्थानिक रोजगार निर्माण करण्याची अपेक्षा करतो. आम्ही तुमच्या त्वरित प्रतिसादाची आणि मार्गदर्शनाची वाट पाहत आहोत.

आपला विश्वासू,
${sender}`
  };

  const originalText = originalTexts[language];
  const translatedText = language !== 'en' ? originalTexts['en'] : null; // For mock, translated is just the English original

  const investmentAmountMatch = originalText.match(/\$([\d.]+)\s*million/);
  const investmentAmount = investmentAmountMatch ? parseFloat(investmentAmountMatch[1]) : null;

  return {
    id: `MIDC-${id.toString().padStart(3, '0')}`,
    sender,
    originalText,
    translatedText,
    language,
    industry,
    intent,
    priority,
    confidence: parseFloat((Math.random() * 0.3 + 0.7).toFixed(2)), // 70-100% confidence
    assignedTo: assigned,
    entities: {
      investorName: sender,
      investmentAmount: investmentAmount ? `$${investmentAmount} million` : 'N/A',
      location: location,
    },
  };
};

const mockDetailedInquiries = Array.from({ length: 15 }, (_, i) => generateDetailedInquiry(i + 1));

const getPriorityTagClass = (priority) => {
  switch (priority) {
    case 'High': return styles.priorityHighTag;
    case 'Medium': return styles.priorityMediumTag;
    case 'Low': return styles.priorityLowTag;
    case 'Informational': return styles.priorityInformationalTag;
    default: return '';
  }
};

const InquiryDetail = ({ inquiryId, onClose }) => {
  const [inquiry, setInquiry] = useState(null);
  const [showOriginal, setShowOriginal] = useState(true);

  useEffect(() => {
    if (inquiryId) {
      // In a real app, you'd fetch this from an API
      const foundInquiry = mockDetailedInquiries.find(inv => inv.id === inquiryId);
      setInquiry(foundInquiry);
      if (foundInquiry && foundInquiry.language !== 'en') {
        setShowOriginal(true); // Default to original if not English
      } else {
        setShowOriginal(true); // Default to original if English
      }
    } else {
      setInquiry(null);
    }
  }, [inquiryId]);

  if (!inquiry) {
    return null; // Or a loading spinner
  }

  const displayInquiryText = (inquiry.language !== 'en' && !showOriginal && inquiry.translatedText)
    ? inquiry.translatedText
    : inquiry.originalText;

  return (
    <div className={`${styles.inquiryDetailOverlay} ${inquiryId ? styles.isOpen : ''}`}>
      <div className={styles.inquiryDetailPanel}>
        <div className={styles.header}>
          <h2>Inquiry {inquiry.id}</h2>
          <button onClick={onClose} className={styles.closeButton}>
            <X size={24} />
          </button>
        </div>

        <div className={styles.content}>
          {/* Full Inquiry Text */}
          <div className={styles.section}>
            <h3 className={styles.sectionTitle}>Inquiry Text</h3>
            {inquiry.language !== 'en' && inquiry.translatedText && (
              <div className={styles.textToggle}>
                <button
                  className={`${styles.textToggleButton} ${showOriginal ? styles.active : ''}`}
                  onClick={() => setShowOriginal(true)}
                >
                  View Original ({inquiry.language.toUpperCase()})
                </button>
                <button
                  className={`${styles.textToggleButton} ${!showOriginal ? styles.active : ''}`}
                  onClick={() => setShowOriginal(false)}
                >
                  View Translation (EN)
                </button>
              </div>
            )}
            <p className={styles.inquiryFullText}>{displayInquiryText}</p>
          </div>

          {/* Extracted Entities */}
          <div className={styles.section}>
            <h3 className={styles.sectionTitle}>Extracted Entities</h3>
            <div className={styles.entityItem}>
              <span className={styles.entityLabel}>Investor Name:</span>
              <span className={styles.entityValue}>{inquiry.entities.investorName}</span>
            </div>
            <div className={styles.entityItem}>
              <span className={styles.entityLabel}>Investment Amount:</span>
              <span className={styles.entityValue}>{inquiry.entities.investmentAmount}</span>
            </div>
            <div className={styles.entityItem}>
              <span className={styles.entityLabel}>Location:</span>
              <span className={styles.entityValue}>{inquiry.entities.location}</span>
            </div>
          </div>

          {/* Classification Block */}
          <div className={styles.section}>
            <h3 className={styles.sectionTitle}>Classification</h3>
            <div className={styles.classificationGrid}>
              <span className={styles.classificationLabel}>Primary Intent:</span>
              <span className={styles.classificationValue}>{inquiry.intent}</span>

              <span className={styles.classificationLabel}>Industry:</span>
              <span className={styles.classificationValue}>{inquiry.industry}</span>

              <span className={styles.classificationLabel}>Priority:</span>
              <span className={`${styles.priorityTag} ${getPriorityTagClass(inquiry.priority)}`}>{inquiry.priority}</span>

              <span className={styles.classificationLabel}>Confidence:</span>
              <div className={styles.confidenceBarContainer}>
                <div className={styles.confidenceBar} style={{ width: `${inquiry.confidence * 100}%` }}></div>
              </div>
            </div>
          </div>

          {/* Routing Status */}
          <div className={styles.section}>
            <h3 className={styles.sectionTitle}>Routing Status</h3>
            <span className={styles.routingStatusValue}>Assigned to: {inquiry.assignedTo}</span>
          </div>
        </div>

        {/* Action Buttons */}
        <div className={styles.actionButtons}>
          <button className={`${styles.actionButton} ${styles.secondary}`}>Reassign</button>
          <button className={`${styles.actionButton} ${styles.primary}`}>Mark Resolved</button>
          <button className={`${styles.actionButton} ${styles.escalate}`}>Escalate</button>
          <div className={styles.correctClassificationLink}>
            <a href="#" onClick={(e) => { e.preventDefault(); alert('Feedback mechanism not yet implemented.'); }}>Correct this classification</a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InquiryDetail;
