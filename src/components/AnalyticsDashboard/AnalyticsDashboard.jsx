import React, { useMemo } from 'react';
import styles from './AnalyticsDashboard.module.css';
import {
  ResponsiveContainer,
  AreaChart, Area,
  BarChart, Bar,
  PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend
} from 'recharts';
import { ArrowUp, ArrowDown, Minus } from 'lucide-react';
import { mockAnalytics } from '../../data/mockAnalytics'; // Import mock analytics data

// --- Design Tokens & Constants ---
// These are now primarily defined in src/styles/tokens.css and accessed via CSS variables.
// Recharts components need direct color values, so we'll define a subset here.
const RECHARTS_COLORS = {
  bg: 'var(--color-bg)',
  surface: 'var(--color-surface)',
  border: 'var(--color-border)',
  ink: 'var(--color-ink)',
  inkMuted: 'var(--color-ink-muted)',
  sage: 'var(--color-sage)',
  sageDeep: 'var(--color-sage-deep)',
  clay: 'var(--color-clay)',
  clayDeep: 'var(--color-clay-deep)',
  slate: 'var(--color-slate)',
  slateDeep: 'var(--color-slate-deep)',
  gold: 'var(--color-gold)',
};

// Chart Palette (sampling sage/clay/slate/gold)
const CHART_PALETTE = [
  RECHARTS_COLORS.sageDeep,
  RECHARTS_COLORS.clayDeep,
  RECHARTS_COLORS.slateDeep,
  RECHARTS_COLORS.gold,
  RECHARTS_COLORS.sage,
  RECHARTS_COLORS.clay,
  RECHARTS_COLORS.slate,
];

// KPI Target Values (from Section 10 of scoping doc)
const KPI_TARGETS = {
  accuracy: 0.90, // >= 90%
  cacheHitRate: 0.40, // >= 40%
  avgResponseTime: 2 * 60 * 1000, // < 2 minutes in ms
  misroutingRate: 0.05, // < 5%
};

// --- Stat Card Component ---
const StatCard = ({ label, value, unit, targetMet, trend, formatValue }) => {
  const valueClass = targetMet ? styles.targetMet : styles.targetBelow;
  let TrendIcon = Minus;
  let trendClass = styles.flat;
  if (trend > 0) { TrendIcon = ArrowUp; trendClass = styles.up; }
  if (trend < 0) { TrendIcon = ArrowDown; trendClass = styles.down; }

  return (
    <div className={styles.statCard}>
      <div className={styles.statLabel}>{label}</div>
      <div className={styles.statValueContainer}>
        <div className={`${styles.statValue} ${valueClass}`}>
          {formatValue ? formatValue(value) : `${(value * 100).toFixed(1)}${unit}`}
        </div>
        <TrendIcon size={20} className={`${styles.trendArrow} ${trendClass}`} />
      </div>
    </div>
  );
};

const AnalyticsDashboard = () => {
  const { inquiryVolumeOverTime, kpis, intentCounts, languageDistribution } = mockAnalytics;

  // Extract industries from the first day's data, excluding 'date' and 'total'
  const allIndustries = useMemo(() => {
    if (inquiryVolumeOverTime.length === 0) return [];
    return Object.keys(inquiryVolumeOverTime[0]).filter(key => key !== 'date' && key !== 'total');
  }, [inquiryVolumeOverTime]);

  // Memoize top 5 industries for the stacked area chart
  const top5Industries = useMemo(() => {
    const industryTotals = {};
    inquiryVolumeOverTime.forEach(day => {
      allIndustries.forEach(ind => {
        industryTotals[ind] = (industryTotals[ind] || 0) + (day[ind] || 0);
      });
    });
    return Object.entries(industryTotals)
      .sort(([, a], [, b]) => b - a)
      .slice(0, 5)
      .map(([ind]) => ind);
  }, [inquiryVolumeOverTime, allIndustries]);

  // Custom Tooltip for Recharts
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className={styles.rechartsTooltipWrapper}>
          <p className={styles.rechartsTooltipLabel}>{label}</p>
          {payload.map((entry, index) => (
            <p key={`item-${index}`} className={styles.rechartsTooltipItem} style={{ color: entry.color }}>
              {entry.name}: {entry.value}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className={styles.analyticsDashboard}>
      {/* Top Row: Stat Cards */}
      <div className={styles.statCards}>
        <StatCard
          label="Classification Accuracy"
          value={kpis.accuracy.current}
          unit="%"
          targetMet={kpis.accuracy.current >= KPI_TARGETS.accuracy}
          trend={kpis.accuracy.current - kpis.accuracy.prev}
          formatValue={(val) => `${(val * 100).toFixed(1)}%`}
        />
        <StatCard
          label="Cache Hit Rate"
          value={kpis.cacheHitRate.current}
          unit="%"
          targetMet={kpis.cacheHitRate.current >= KPI_TARGETS.cacheHitRate}
          trend={kpis.cacheHitRate.current - kpis.cacheHitRate.prev}
          formatValue={(val) => `${(val * 100).toFixed(1)}%`}
        />
        <StatCard
          label="Avg. Routine Response Time"
          value={kpis.avgResponseTime.current}
          unit=""
          targetMet={kpis.avgResponseTime.current < KPI_TARGETS.avgResponseTime}
          trend={kpis.avgResponseTime.prev - kpis.avgResponseTime.current} // Lower is better, so prev - current
          formatValue={(val) => `${(val / (60 * 1000)).toFixed(1)} min`}
        />
        <StatCard
          label="Misrouting Rate"
          value={kpis.misroutingRate.current}
          unit="%"
          targetMet={kpis.misroutingRate.current < KPI_TARGETS.misroutingRate}
          trend={kpis.misroutingRate.prev - kpis.misroutingRate.current} // Lower is better
          formatValue={(val) => `${(val * 100).toFixed(1)}%`}
        />
      </div>

      {/* Inquiry Volume over 30 days (Stacked Area Chart) */}
      <div className={styles.chartRow}>
        <div className={styles.chartContainer}>
          <h3 className={styles.chartTitle}>Inquiry Volume (Last 30 Days)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={inquiryVolumeOverTime}>
              <CartesianGrid strokeDasharray="3 3" stroke={RECHARTS_COLORS.border} />
              <XAxis dataKey="date" tickFormatter={(dateStr) => new Date(dateStr).getDate()} stroke={RECHARTS_COLORS.inkMuted} />
              <YAxis stroke={RECHARTS_COLORS.inkMuted} />
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ fontFamily: 'var(--font-body)', fontSize: '0.9em', color: RECHARTS_COLORS.inkMuted }} />
              {top5Industries.map((ind, index) => (
                <Area
                  key={ind}
                  type="monotone"
                  dataKey={ind}
                  stackId="1"
                  stroke={CHART_PALETTE[index % CHART_PALETTE.length]}
                  fill={CHART_PALETTE[index % CHART_PALETTE.length]}
                  name={ind}
                  fillOpacity={0.8}
                />
              ))}
              {/* "Other" category for remaining industries */}
              <Area
                type="monotone"
                dataKey={(data) => {
                  let otherSum = 0;
                  allIndustries.forEach(ind => {
                    if (!top5Industries.includes(ind)) {
                      otherSum += data[ind] || 0;
                    }
                  });
                  return otherSum;
                }}
                stackId="1"
                stroke={CHART_PALETTE[top5Industries.length % CHART_PALETTE.length]}
                fill={CHART_PALETTE[top5Industries.length % CHART_PALETTE.length]}
                name="Other Industries"
                fillOpacity={0.8}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Language Distribution (Donut Chart) */}
        <div className={styles.chartContainer}>
          <h3 className={styles.chartTitle}>Language Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={languageDistribution}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={90}
                fill="#8884d8"
                paddingAngle={5}
                dataKey="value"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              >
                {languageDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={CHART_PALETTE[index % CHART_PALETTE.length]} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ fontFamily: 'var(--font-body)', fontSize: '0.9em', color: RECHARTS_COLORS.inkMuted }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Inquiry Count by Primary Intent (Horizontal Bar Chart) */}
      <div className={styles.chartContainer}>
        <h3 className={styles.chartTitle}>Inquiry Count by Primary Intent</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart
            data={intentCounts}
            layout="vertical"
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke={RECHARTS_COLORS.border} horizontal={false} />
            <XAxis type="number" stroke={RECHARTS_COLORS.inkMuted} />
            <YAxis dataKey="name" type="category" stroke={RECHARTS_COLORS.inkMuted} width={120} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="count" fill={RECHARTS_COLORS.sageDeep} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;
