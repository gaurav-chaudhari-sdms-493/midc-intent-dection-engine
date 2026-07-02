import React, { useState, useEffect } from 'react';
import styles from './Layout.module.css';
import { Inbox, Route, BarChart2, Book, Settings } from 'lucide-react';
import { mockInquiries } from '../../data/mockInquiries'; // Import mock inquiries

const navItems = [
  { name: 'Inbox', icon: Inbox, page: 'Inbox' },
  { name: 'Routing', icon: Route, page: 'Routing' },
  { name: 'Analytics', icon: BarChart2, page: 'Analytics' },
  { name: 'Taxonomy', icon: Book, page: 'Taxonomy' },
  { name: 'Settings', icon: Settings, page: 'Settings' },
];

const Layout = ({ pageTitle, children, onNavigate }) => {
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [activeNav, setActiveNav] = useState('Inbox');

  // Calculate pending high-priority count from mock data
  const pendingHighPriorityCount = mockInquiries.filter(
    (inquiry) => inquiry.priority === 'High' && inquiry.routing_status !== 'Resolved'
  ).length;

  const officerName = "Officer Jane Doe";
  const officerInitials = "JD";

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 900) {
        setIsSidebarCollapsed(true);
      } else {
        setIsSidebarCollapsed(false);
      }
    };

    window.addEventListener('resize', handleResize);
    handleResize(); // Set initial state

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const handleNavClick = (pageName) => {
    setActiveNav(pageName);
    onNavigate(pageName);
  };

  return (
    <div className={styles.layout}>
      <aside className={`${styles.sidebar} ${isSidebarCollapsed ? styles.collapsed : ''}`}>
        <div className={styles.logoPlaceholder}>
          {!isSidebarCollapsed && "MIDC"}
        </div>
        <nav className={styles.nav}>
          {navItems.map((item) => (
            <a
              key={item.name}
              href="#"
              className={`${styles.navItem} ${activeNav === item.page ? styles.active : ''}`}
              onClick={(e) => {
                e.preventDefault();
                handleNavClick(item.page);
              }}
            >
              <item.icon size={20} />
              <span>{!isSidebarCollapsed && item.name}</span>
            </a>
          ))}
        </nav>
      </aside>

      <div className={styles.mainContentArea}>
        <header className={styles.topbar}>
          <h1 className={styles.pageTitle}>{pageTitle}</h1>
          <div className={styles.userInfo}>
            {pendingHighPriorityCount > 0 && (
              <span className={styles.priorityBadge}>
                {pendingHighPriorityCount} pending high-priority
              </span>
            )}
            <span>{officerName}</span>
            <div className={styles.avatar}>{officerInitials}</div>
          </div>
        </header>
        <main className={styles.content}>
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;
