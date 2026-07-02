import React, { useState } from 'react';
import Layout from './components/Layout/Layout';
import InquiryInbox from './components/InquiryInbox/InquiryInbox';
import InquiryDetail from './components/InquiryDetail/InquiryDetail';
import AnalyticsDashboard from './components/AnalyticsDashboard/AnalyticsDashboard';
import TaxonomyManager from './components/TaxonomyManager/TaxonomyManager';
import RoutingQueue from './components/RoutingQueue/RoutingQueue';
import Settings from './components/Settings/Settings'; // Import Settings

function App() {
  const [selectedInquiryId, setSelectedInquiryId] = useState(null);
  const [currentPage, setCurrentPage] = useState('Inbox');

  const handleInquirySelect = (id) => {
    setSelectedInquiryId(id);
  };

  const handleCloseDetail = () => {
    setSelectedInquiryId(null);
  };

  const handleNavigate = (pageName) => {
    setCurrentPage(pageName);
    setSelectedInquiryId(null); // Close detail view when navigating
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'Inbox':
        return <InquiryInbox onInquirySelect={handleInquirySelect} />;
      case 'Routing':
        return <RoutingQueue onInquirySelect={handleInquirySelect} />;
      case 'Analytics':
        return <AnalyticsDashboard />;
      case 'Taxonomy':
        return <TaxonomyManager />;
      case 'Settings': // Add case for Settings
        return <Settings />;
      default:
        return <InquiryInbox onInquirySelect={handleInquirySelect} />;
    }
  };

  return (
    <Layout pageTitle={currentPage} onNavigate={handleNavigate}>
      {renderPage()}
      <InquiryDetail inquiryId={selectedInquiryId} onClose={handleCloseDetail} />
    </Layout>
  );
}

export default App;
