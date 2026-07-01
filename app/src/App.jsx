import {
  ArrowLeft,
  ArrowRight,
  BadgeInfo,
  BarChart3,
  BookOpen,
  Building2,
  CalendarDays,
  CheckCircle2,
  Database,
  Download,
  Gauge,
  GitBranch,
  Layers3,
  LineChart,
  Menu,
  RefreshCw,
  Search,
  ShieldCheck,
  SlidersHorizontal,
  Target,
  Users,
  XCircle,
} from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import predictions from "../../data/processed/new1_predictions.json";
import metrics from "../../data/processed/model_metrics.json";

const PAGE_SIZES = [25, 50, 100, "all"];

const navItems = [
  { path: "/", label: "Tổng quan" },
  { path: "/screener", label: "Sàng lọc" },
  { path: "/model", label: "Mô hình" },
  { path: "/data", label: "Dữ liệu" },
  { path: "/limitations", label: "Giới hạn" },
];

const resourceLinks = [
  {
    label: "Feature-set 258",
    href: "/resources/new1_features_258.csv",
    note: "Danh sách feature của member 258",
  },
  {
    label: "Feature-set 309",
    href: "/resources/new1_features_309.csv",
    note: "Danh sách feature của member 309",
  },
  {
    label: "Model card",
    href: "/resources/model_card.md",
    note: "Giải thích NEW1, training và scoring",
  },
  {
    label: "Prediction sample",
    href: "/resources/predictions_sample.csv",
    note: "Mẫu CSV nhỏ dùng cho demo/documentation",
  },
];

const formatPercent = (value) => `${(value * 100).toFixed(2)}%`;
const formatProbability = (value) => Number(value).toFixed(2);

function normalizeHash(hash) {
  const value = hash.replace(/^#/, "") || "/";
  return navItems.some((item) => item.path === value) ? value : "/";
}

function useHashRoute() {
  const [route, setRoute] = useState(() => normalizeHash(window.location.hash));

  useEffect(() => {
    const onHashChange = () => setRoute(normalizeHash(window.location.hash));
    window.addEventListener("hashchange", onHashChange);
    return () => window.removeEventListener("hashchange", onHashChange);
  }, []);

  return route;
}

function routeHref(path) {
  return `#${path}`;
}

function Badge({ value }) {
  const risk = value === "Risk";
  return <span className={`badge ${risk ? "badge-risk" : "badge-safe"}`}>{value}</span>;
}

function CorrectnessBadge({ value }) {
  return (
    <span className={`badge ${value ? "badge-correct" : "badge-wrong"}`}>
      {value ? "Đúng" : "Sai"}
    </span>
  );
}

function StatCard({ icon: Icon, value, label }) {
  return (
    <article className="stat-card">
      <span className="icon-box">
        <Icon size={28} strokeWidth={1.8} />
      </span>
      <div>
        <strong>{value}</strong>
        <span>{label}</span>
      </div>
    </article>
  );
}

function MetricCard({ icon: Icon, label, value }) {
  return (
    <article className="metric-card">
      <span className="metric-icon">
        <Icon size={25} strokeWidth={1.8} />
      </span>
      <span>{label}</span>
      <strong>{value}</strong>
    </article>
  );
}

function Header({ route }) {
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    setMenuOpen(false);
  }, [route]);

  return (
    <header className="topbar">
      <a className="brand" href={routeHref("/")} aria-label="Banking Risk Screener">
        <Building2 size={23} />
        <span>Banking Risk Screener</span>
      </a>
      <nav className="desktop-nav" aria-label="Điều hướng chính">
        {navItems.map((item) => (
          <a className={route === item.path ? "active" : ""} key={item.path} href={routeHref(item.path)}>
            {item.label}
          </a>
        ))}
      </nav>
      <button
        className="menu-button"
        aria-expanded={menuOpen}
        aria-label="Mở menu"
        onClick={() => setMenuOpen((value) => !value)}
      >
        <Menu size={22} />
      </button>
      {menuOpen && (
        <nav className="mobile-nav" aria-label="Điều hướng mobile">
          {navItems.map((item) => (
            <a className={route === item.path ? "active" : ""} key={item.path} href={routeHref(item.path)}>
              {item.label}
            </a>
          ))}
        </nav>
      )}
    </header>
  );
}

function Hero() {
  return (
    <section className="panel hero-panel">
      <div className="hero-copy">
        <p className="eyebrow">Tổng quan</p>
        <h1>Bộ lọc rủi ro lợi nhuận cổ phiếu ngân hàng Việt Nam</h1>
        <p>
          Dashboard demo dùng kết quả NEW1 để xem các bank-quarter được mô hình gắn nhãn
          Risk hoặc NoRisk cho quý tiếp theo.
        </p>
        <span className="disclaimer-pill">Không phải khuyến nghị mua/bán</span>
        <div className="action-row">
          <a className="primary-action" href={routeHref("/screener")}>
            Xem toàn bộ bảng <ArrowRight size={18} />
          </a>
          <a className="ghost-action" href={routeHref("/model")}>
            Tìm hiểu mô hình
          </a>
        </div>
      </div>
      <div className="bank-visual" aria-hidden="true">
        <div className="columns">
          <span />
          <span />
          <span />
          <span />
          <span />
        </div>
        <Building2 size={122} strokeWidth={1.2} />
      </div>
      <div className="hero-stats">
        <StatCard icon={Building2} value={metrics.dataset.banks} label="mã ngân hàng" />
        <StatCard icon={Database} value="1.202" label="quan sát" />
        <StatCard icon={Search} value={metrics.dataset.test_rows} label="kết quả NEW1" />
      </div>
    </section>
  );
}

function HomeView() {
  const performance = metrics.test_at_rapidminer_threshold;
  const risk = performance.per_class.Risk;
  const previewRows = predictions.slice(0, 6);

  return (
    <>
      <Hero />
      <section className="panel">
        <div className="section-heading">
          <p className="eyebrow">MVP snapshot</p>
          <h2>NEW1 là mô hình chính của demo</h2>
          <p>
            Trang chính chỉ giữ phần tóm tắt. Bảng đầy đủ, giải thích mô hình và phần dữ
            liệu được tách sang các view riêng để dễ đọc hơn.
          </p>
        </div>
        <div className="metric-grid home-metrics">
          <MetricCard icon={Target} label="Accuracy" value={formatPercent(performance.accuracy)} />
          <MetricCard icon={BarChart3} label="Risk precision" value={formatPercent(risk.precision)} />
          <MetricCard icon={LineChart} label="Risk recall" value={formatPercent(risk.recall)} />
          <MetricCard icon={Gauge} label="Macro-F1" value={formatPercent(performance.macro_f1)} />
        </div>
      </section>
      <section className="panel">
        <div className="section-heading split-heading">
          <div>
            <p className="eyebrow">Preview</p>
            <h2>Một vài dòng sàng lọc</h2>
          </div>
          <a className="secondary-action" href={routeHref("/screener")}>
            Xem toàn bộ <ArrowRight size={16} />
          </a>
        </div>
        <PredictionTable rows={previewRows} />
      </section>
      <section className="quick-links">
        <a className="quick-link-card" href={routeHref("/model")}>
          <GitBranch size={28} />
          <div>
            <h3>Model journey</h3>
            <p>OLD1/OLD2/OLD3, NEW1 và NEW2 được giải thích ở trang mô hình.</p>
          </div>
        </a>
        <a className="quick-link-card" href={routeHref("/data")}>
          <Layers3 size={28} />
          <div>
            <h3>Dữ liệu & Feature</h3>
            <p>Feature-set 258/309 và các nhóm biến được tách sang trang riêng.</p>
          </div>
        </a>
        <a className="quick-link-card" href={routeHref("/limitations")}>
          <ShieldCheck size={28} />
          <div>
            <h3>Giới hạn</h3>
            <p>Ghi rõ đây là demo screening, không phải khuyến nghị đầu tư.</p>
          </div>
        </a>
      </section>
    </>
  );
}

function PredictionTable({ rows }) {
  return (
    <div className="table-shell">
      <table>
        <thead>
          <tr>
            <th>Mã</th>
            <th>Feature quý</th>
            <th>Target quý</th>
            <th>Điểm</th>
            <th>Dự đoán</th>
            <th>Thực tế</th>
            <th>Đánh giá</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.row_key}>
              <td>{row.ticker}</td>
              <td>{row.feature_quarter}</td>
              <td>{row.target_quarter}</td>
              <td>{formatProbability(row.ensemble_probability)}</td>
              <td>
                <Badge value={row.prediction} />
              </td>
              <td>
                <Badge value={row.actual} />
              </td>
              <td>
                <CorrectnessBadge value={row.is_correct} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {rows.length === 0 && <p className="empty-state">Không có dòng phù hợp.</p>}
    </div>
  );
}

function ScreenerView() {
  const [ticker, setTicker] = useState("all");
  const [quarter, setQuarter] = useState("all");
  const [prediction, setPrediction] = useState("all");
  const [actual, setActual] = useState("all");
  const [correctness, setCorrectness] = useState("all");
  const [pageSize, setPageSize] = useState(25);
  const [page, setPage] = useState(1);

  const tickers = useMemo(() => [...new Set(predictions.map((row) => row.ticker))], []);
  const quarters = useMemo(() => [...new Set(predictions.map((row) => row.target_quarter))], []);

  const filteredRows = useMemo(
    () =>
      predictions.filter((row) => {
        const byTicker = ticker === "all" || row.ticker === ticker;
        const byQuarter = quarter === "all" || row.target_quarter === quarter;
        const byPrediction = prediction === "all" || row.prediction === prediction;
        const byActual = actual === "all" || row.actual === actual;
        const byCorrectness =
          correctness === "all" ||
          (correctness === "correct" && row.is_correct) ||
          (correctness === "wrong" && !row.is_correct);
        return byTicker && byQuarter && byPrediction && byActual && byCorrectness;
      }),
    [ticker, quarter, prediction, actual, correctness]
  );

  const riskPredictions = filteredRows.filter((row) => row.prediction === "Risk").length;
  const correctRows = filteredRows.filter((row) => row.is_correct).length;
  const wrongRows = filteredRows.length - correctRows;
  const allMode = pageSize === "all";
  const totalPages = allMode ? 1 : Math.max(1, Math.ceil(filteredRows.length / pageSize));
  const safePage = Math.min(page, totalPages);
  const pagedRows = allMode
    ? filteredRows
    : filteredRows.slice((safePage - 1) * pageSize, safePage * pageSize);

  const resetFilters = () => {
    setTicker("all");
    setQuarter("all");
    setPrediction("all");
    setActual("all");
    setCorrectness("all");
    setPageSize(25);
    setPage(1);
  };

  const onFilterChange = (setter) => (event) => {
    setter(event.target.value);
    setPage(1);
  };

  const onPageSizeChange = (event) => {
    const value = event.target.value === "all" ? "all" : Number(event.target.value);
    setPageSize(value);
    setPage(1);
  };

  return (
    <section className="panel page-panel">
      <div className="section-heading">
        <p className="eyebrow">Sàng lọc NEW1</p>
        <h1>Kết quả dự đoán Risk / NoRisk</h1>
        <p>
          Trang này hiển thị toàn bộ 234 dòng NEW1 test output. Không có live
          prediction hoặc retraining ở bước này.
        </p>
      </div>
      <div className="summary-grid">
        <StatCard icon={Database} value={filteredRows.length} label="dòng phù hợp" />
        <StatCard icon={Target} value={riskPredictions} label="dự đoán Risk" />
        <StatCard icon={CheckCircle2} value={correctRows} label="dòng đúng" />
        <StatCard icon={XCircle} value={wrongRows} label="dòng sai" />
      </div>
      <div className="filters" aria-label="Bộ lọc bảng sàng lọc">
        <label>
          Mã cổ phiếu
          <select value={ticker} onChange={onFilterChange(setTicker)}>
            <option value="all">Tất cả</option>
            {tickers.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </label>
        <label>
          Quý
          <select value={quarter} onChange={onFilterChange(setQuarter)}>
            <option value="all">Tất cả</option>
            {quarters.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </label>
        <label>
          Dự đoán
          <select value={prediction} onChange={onFilterChange(setPrediction)}>
            <option value="all">Tất cả</option>
            <option value="Risk">Risk</option>
            <option value="NoRisk">NoRisk</option>
          </select>
        </label>
        <label>
          Thực tế
          <select value={actual} onChange={onFilterChange(setActual)}>
            <option value="all">Tất cả</option>
            <option value="Risk">Risk</option>
            <option value="NoRisk">NoRisk</option>
          </select>
        </label>
        <label>
          Đánh giá
          <select value={correctness} onChange={onFilterChange(setCorrectness)}>
            <option value="all">Tất cả</option>
            <option value="correct">Đúng</option>
            <option value="wrong">Sai</option>
          </select>
        </label>
        <label>
          Hiển thị
          <select value={pageSize} onChange={onPageSizeChange}>
            {PAGE_SIZES.map((value) => (
              <option key={value} value={value}>
                {value === "all" ? "Tất cả" : `${value} dòng`}
              </option>
            ))}
          </select>
        </label>
        <button type="button" onClick={resetFilters}>
          Làm mới <RefreshCw size={15} />
        </button>
      </div>
      <PredictionTable rows={pagedRows} />
      <div className="table-footer">
        <p>
          Hiển thị {pagedRows.length} / {filteredRows.length} dòng phù hợp từ{" "}
          {predictions.length} kết quả NEW1.
        </p>
        {!allMode && (
          <div className="pagination">
            <button type="button" disabled={safePage <= 1} onClick={() => setPage((value) => Math.max(1, value - 1))}>
              <ArrowLeft size={16} /> Trang trước
            </button>
            <span>
              Trang {safePage} / {totalPages}
            </span>
            <button
              type="button"
              disabled={safePage >= totalPages}
              onClick={() => setPage((value) => Math.min(totalPages, value + 1))}
            >
              Trang sau <ArrowRight size={16} />
            </button>
          </div>
        )}
      </div>
    </section>
  );
}

function ModelView() {
  const performance = metrics.test_at_rapidminer_threshold;
  const risk = performance.per_class.Risk;

  return (
    <section className="panel page-panel">
      <div className="section-heading">
        <p className="eyebrow">Mô hình</p>
        <h1>Mô hình chính: NEW1</h1>
        <p>
          NEW1 là ensemble hai member feature-set 258 và 309. Mỗi member học từ
          auxiliary Risk5, sau đó web demo đánh giá và hiển thị theo target Risk10.
        </p>
      </div>
      <div className="metric-grid">
        <MetricCard icon={Target} label="Accuracy" value={formatPercent(performance.accuracy)} />
        <MetricCard icon={BarChart3} label="Risk precision" value={formatPercent(risk.precision)} />
        <MetricCard icon={LineChart} label="Risk recall" value={formatPercent(risk.recall)} />
        <MetricCard icon={Gauge} label="Macro-F1" value={formatPercent(performance.macro_f1)} />
        <MetricCard icon={SlidersHorizontal} label="Threshold" value={metrics.threshold.toFixed(3)} />
      </div>
      <div className="model-story">
        <aside className="note-card">
          <BadgeInfo size={26} />
          <div>
            <h3>Cách đọc NEW1</h3>
            <p>
              Output là xác suất Risk. Nếu xác suất lớn hơn hoặc bằng 0.437, dòng đó
              được gắn nhãn Risk. Đây là tín hiệu sàng lọc để analyst xem tiếp.
            </p>
          </div>
        </aside>
        <aside className="note-card">
          <Layers3 size={26} />
          <div>
            <h3>Vì sao chọn NEW1?</h3>
            <p>
              NEW1 có câu chuyện đơn giản nhất cho MVP: một bộ dữ liệu, một ensemble,
              một threshold cố định và output dễ đưa lên web tĩnh.
            </p>
          </div>
        </aside>
      </div>
      <div className="history-block">
        <div className="section-heading compact">
          <p className="eyebrow">Model journey</p>
          <h2>Các mô hình đã thử</h2>
        </div>
        <div className="history-grid">
          {metrics.model_history.map((model) => (
            <article className={`history-card ${model.id === "NEW1" ? "selected" : ""}`} key={model.id}>
              <span className="model-id">{model.id}</span>
              <h3>{model.name}</h3>
              <p>{model.role}</p>
              <dl>
                <div>
                  <dt>Task</dt>
                  <dd>{model.task}</dd>
                </div>
                <div>
                  <dt>Test accuracy</dt>
                  <dd>{formatPercent(model.test_accuracy)}</dd>
                </div>
                {model.risk_recall !== undefined && (
                  <div>
                    <dt>Risk recall</dt>
                    <dd>{formatPercent(model.risk_recall)}</dd>
                  </div>
                )}
              </dl>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

function DataFeatureView() {
  return (
    <section className="panel page-panel data-page">
      <div className="section-heading">
        <p className="eyebrow">Dữ liệu & Feature</p>
        <h1>Mô hình nhìn thấy gì?</h1>
        <p>
          Trang này tách riêng phần dữ liệu để tránh làm dashboard chính bị rối. Mỗi
          observation là một bank-quarter.
        </p>
      </div>
      <div className="data-story-grid">
        <article className="explain-card">
          <Database size={30} />
          <h3>Data grain</h3>
          <p>
            Mỗi dòng tương ứng một ngân hàng tại một quý. Dữ liệu chính có 1.202
            observations và 26 mã ngân hàng.
          </p>
        </article>
        <article className="explain-card">
          <CalendarDays size={30} />
          <h3>Feature t → Target t+1</h3>
          <p>
            Feature được lấy tại quý t. Target đánh dấu rủi ro lợi nhuận ở quý kế
            tiếp, tức t+1.
          </p>
        </article>
      </div>
      <div className="feature-facts">
        <StatCard icon={Layers3} value={metrics.feature_counts.member_258} label="feature-set 258" />
        <StatCard icon={Layers3} value={metrics.feature_counts.member_309} label="feature-set 309" />
        <StatCard icon={GitBranch} value={metrics.feature_counts.union} label="feature union" />
        <StatCard icon={CheckCircle2} value={metrics.feature_counts.overlap} label="feature overlap" />
      </div>
      <div className="feature-explain-grid">
        <article className="explain-card wide">
          <h3>Feature-set 258 và 309 là gì?</h3>
          <p>
            Đây là hai nhóm biến được giữ lại từ workflow RapidMiner cũ. NEW1 train
            hai member riêng, mỗi member dùng một feature-set, rồi trung bình xác
            suất Risk để ra điểm ensemble cuối cùng.
          </p>
        </article>
        <article className="explain-card">
          <h3>Union 357</h3>
          <p>357 feature khác nhau xuất hiện trong ít nhất một member.</p>
        </article>
        <article className="explain-card">
          <h3>Overlap 210</h3>
          <p>210 feature xuất hiện trong cả hai member, tạo phần lõi chung.</p>
        </article>
      </div>
      <div className="section-heading compact">
        <p className="eyebrow">Feature groups</p>
        <h2>Nhóm biến chính</h2>
      </div>
      <div className="feature-groups">
        {metrics.feature_groups.map((group) => (
          <article className="feature-group-card" key={group.name}>
            <BookOpen size={22} />
            <div>
              <h3>{group.name}</h3>
              <p>{group.description}</p>
            </div>
          </article>
        ))}
      </div>
      <div className="section-heading compact">
        <p className="eyebrow">Resources</p>
        <h2>Tải file tham khảo</h2>
      </div>
      <div className="resource-grid">
        {resourceLinks.map((item) => (
          <a className="resource-card" href={item.href} download key={item.href}>
            <Download size={24} />
            <div>
              <h3>{item.label}</h3>
              <p>{item.note}</p>
            </div>
          </a>
        ))}
      </div>
    </section>
  );
}

function LimitationsView() {
  const items = [
    {
      icon: Database,
      title: "Dữ liệu còn nhỏ",
      text: "Bộ dữ liệu là bank-quarter panel, số quan sát hạn chế.",
    },
    {
      icon: Users,
      title: "Class Risk bị lệch",
      text: "Risk ít hơn NoRisk nên không nên chỉ nhìn accuracy.",
    },
    {
      icon: CalendarDays,
      title: "Chưa mô phỏng đầy đủ ngày công bố",
      text: "MVP demo chưa xử lý lịch công bố báo cáo thực tế như một hệ thống production.",
    },
    {
      icon: Gauge,
      title: "Cần analyst review",
      text: "Kết quả cần được kiểm tra lại với bối cảnh tài chính và thông tin doanh nghiệp.",
    },
    {
      icon: ShieldCheck,
      title: "Không tự động mua bán",
      text: "Không dùng để tự động mua, bán hoặc nắm giữ cổ phiếu.",
    },
    {
      icon: XCircle,
      title: "Không phải live prediction",
      text: "Web hiện là demo đọc kết quả mô hình đã chạy, không retrain hoặc crawl dữ liệu mới.",
    },
  ];

  return (
    <section className="panel page-panel">
      <div className="section-heading">
        <p className="eyebrow">Giới hạn</p>
        <h1>Giới hạn của dự án</h1>
      </div>
      <div className="limitations-grid">
        {items.map((item) => (
          <article className="limitation-card" key={item.title}>
            <item.icon size={34} strokeWidth={1.7} />
            <div>
              <h3>{item.title}</h3>
              <p>{item.text}</p>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

function CurrentView({ route }) {
  if (route === "/screener") return <ScreenerView />;
  if (route === "/model") return <ModelView />;
  if (route === "/data") return <DataFeatureView />;
  if (route === "/limitations") return <LimitationsView />;
  return <HomeView />;
}

export default function App() {
  const route = useHashRoute();

  return (
    <>
      <Header route={route} />
      <main>
        <CurrentView route={route} />
      </main>
    </>
  );
}
