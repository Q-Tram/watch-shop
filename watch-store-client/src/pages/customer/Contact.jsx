
import { useWebsiteSettings } from "../../context/WebsiteSettingsContext";

function Contact() {
  const { settings } = useWebsiteSettings();

  const handleSubmit = (e) => {
    e.preventDefault();
    alert("Cảm ơn bạn đã liên hệ với WatchStore!");
    e.target.reset();
  };

  const siteName = settings?.siteName || "WatchStore";
  const email = settings?.contactEmail || "support@watchstore.com";
  const phone = settings?.contactPhone || "+84 123 456 789";
  const address = settings?.contactAddress || "TP. Hồ Chí Minh";
  const workingHours =
    settings?.workingHours || "Thứ 2 – Thứ 7 | 08:00 – 21:00";
  const slogan = settings?.contactSlogan || "YOUR TIME, YOUR STYLE.";
  const description =
    settings?.footerDescription ||
    "Chúng tôi luôn sẵn sàng lắng nghe và hỗ trợ bạn trong hành trình lựa chọn chiếc đồng hồ hoàn hảo.";

  return (
    <main className="contact-page">
      <style>{`
        .contact-page {
          background: #f5f6f8;
          min-height: 80vh;
          padding: 65px 24px 80px;
          font-family: Arial, sans-serif;
          color: #172337;
          box-sizing: border-box;
        }

        .contact-page * { box-sizing: border-box; }

        .contact-container {
          max-width: 1160px;
          margin: 0 auto;
        }

        .contact-heading {
          text-align: center;
          margin-bottom: 42px;
        }

        .contact-eyebrow,
        .contact-small-title {
          color: #b89558;
          font-size: 12px;
          font-weight: 700;
          letter-spacing: 2.5px;
        }

        .contact-heading h1 {
          font-size: 34px;
          font-weight: 700;
          text-transform: uppercase;
          margin: 13px 0;
          color: #172337;
        }

        .contact-heading p {
          color: #737b87;
          font-size: 15px;
          line-height: 1.7;
          margin: 0;
        }

        .contact-heading-line {
          width: 55px;
          height: 3px;
          background: #bd9855;
          margin: 22px auto 0;
        }

        .contact-layout {
          display: grid;
          grid-template-columns: 0.85fr 1.15fr;
          gap: 25px;
          align-items: stretch;
        }

        .contact-info {
          background: linear-gradient(145deg, #1d2c43, #101b2d);
          border-radius: 14px;
          padding: 42px 38px;
          color: #fff;
          display: flex;
          flex-direction: column;
          justify-content: space-between;
          min-width: 0;
          box-shadow: 0 12px 35px rgba(20, 35, 55, 0.12);
        }

        .contact-info h2 {
          font-size: 30px;
          line-height: 1.35;
          font-weight: 700;
          margin: 17px 0;
          color: #fff;
          overflow-wrap: anywhere;
        }

        .contact-description {
          font-size: 14px;
          line-height: 1.9;
          color: #c5ced9;
          margin-bottom: 35px;
        }

        .contact-details {
          display: flex;
          flex-direction: column;
          gap: 25px;
        }

        .contact-detail {
          display: flex;
          align-items: center;
          gap: 16px;
        }

        .contact-icon {
          width: 46px;
          height: 46px;
          flex-shrink: 0;
          border: 1px solid rgba(189, 152, 85, 0.5);
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          color: #d6b477;
          font-size: 19px;
        }

        .contact-detail span {
          display: block;
          color: #d6b477;
          font-size: 11px;
          font-weight: 700;
          letter-spacing: 1.2px;
          text-transform: uppercase;
          margin-bottom: 7px;
        }

        .contact-detail p,
        .contact-detail a {
          color: #fff;
          font-size: 14px;
          margin: 0;
          line-height: 1.6;
          text-decoration: none;
          overflow-wrap: anywhere;
        }

        .contact-detail a:hover { color: #d6b477; }

        .contact-info-footer {
          border-top: 1px solid rgba(255, 255, 255, 0.2);
          padding-top: 23px;
          margin-top: 38px;
          color: #d6b477;
          font-size: 11px;
          letter-spacing: 2px;
          font-weight: 600;
          overflow-wrap: anywhere;
        }

        .contact-form-card {
          background: #fff;
          border-radius: 14px;
          padding: 42px;
          min-width: 0;
          box-shadow: 0 12px 35px rgba(20, 35, 55, 0.06);
        }

        .contact-form-heading { margin-bottom: 30px; }

        .contact-form-heading h2 {
          color: #172337;
          font-size: 27px;
          font-weight: 700;
          margin: 12px 0;
        }

        .contact-form-heading p {
          color: #7a828d;
          font-size: 14px;
          line-height: 1.7;
          margin: 0;
        }

        .contact-form-group {
          display: flex;
          flex-direction: column;
          gap: 10px;
          margin-bottom: 22px;
        }

        .contact-form-group label {
          font-size: 14px;
          font-weight: 600;
          color: #26354a;
        }

        .contact-form-group input,
        .contact-form-group textarea {
          width: 100%;
          border: 1px solid #e0e4e9;
          border-radius: 7px;
          padding: 14px 16px;
          font-family: Arial, sans-serif;
          font-size: 14px;
          color: #172337;
          background: #fafbfc;
          outline: none;
          transition: border-color 0.2s, box-shadow 0.2s;
        }

        .contact-form-group input { height: 49px; }

        .contact-form-group textarea {
          resize: vertical;
          min-height: 145px;
          line-height: 1.6;
        }

        .contact-form-group input:focus,
        .contact-form-group textarea:focus {
          border-color: #bd9855;
          box-shadow: 0 0 0 3px rgba(189, 152, 85, 0.12);
          background: #fff;
        }

        .contact-form-group input::placeholder,
        .contact-form-group textarea::placeholder {
          color: #a5abb4;
        }

        .contact-submit {
          width: 100%;
          min-height: 51px;
          border: none;
          border-radius: 7px;
          background: #172337;
          color: #fff;
          font-size: 13px;
          font-weight: 700;
          letter-spacing: 1px;
          cursor: pointer;
          transition: all 0.25s;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 12px;
        }

        .contact-submit:hover {
          background: #bd9855;
          transform: translateY(-2px);
        }

        .contact-submit span { font-size: 19px; }

        .contact-form-note {
          margin-top: 24px;
          text-align: center;
          color: #9299a3;
          font-size: 12px;
        }

        .contact-form-note span { color: #bd9855; }

        @media (max-width: 768px) {
          .contact-page { padding: 40px 16px 55px; }
          .contact-heading h1 { font-size: 25px; }
          .contact-layout {
            grid-template-columns: 1fr;
            gap: 18px;
          }
          .contact-info,
          .contact-form-card { padding: 28px 22px; }
          .contact-info h2 { font-size: 25px; }
          .contact-form-heading h2 { font-size: 23px; }
        }

        @media (max-width: 400px) {
          .contact-heading h1 { font-size: 22px; }
          .contact-info,
          .contact-form-card { padding: 24px 18px; }
        }
      `}</style>

      <div className="contact-container">
        <div className="contact-heading">
          <span className="contact-eyebrow">
            {siteName.toUpperCase()} CUSTOMER CARE
          </span>

          <h1>Liên hệ với chúng tôi</h1>

          <p>
            Chúng tôi luôn sẵn sàng lắng nghe và hỗ trợ bạn trong hành trình
            lựa chọn chiếc đồng hồ hoàn hảo.
          </p>

          <div className="contact-heading-line"></div>
        </div>

        <div className="contact-layout">
          <section className="contact-info">
            <div>
              <span className="contact-small-title">GET IN TOUCH</span>

              <h2>
                Hãy kết nối
                <br />
                với {siteName}.
              </h2>

              <p className="contact-description">{description}</p>
            </div>

            <div className="contact-details">
              <div className="contact-detail">
                <div className="contact-icon">✉</div>
                <div>
                  <span>Email</span>
                  <a href={`mailto:${email}`}>{email}</a>
                </div>
              </div>

              <div className="contact-detail">
                <div className="contact-icon">☎</div>
                <div>
                  <span>Điện thoại</span>
                  <a href={`tel:${phone.replace(/\s/g, "")}`}>{phone}</a>
                </div>
              </div>

              <div className="contact-detail">
                <div className="contact-icon">⌖</div>
                <div>
                  <span>Địa chỉ</span>
                  <p>{address}</p>
                </div>
              </div>

              <div className="contact-detail">
                <div className="contact-icon">◷</div>
                <div>
                  <span>Giờ làm việc</span>
                  <p>{workingHours}</p>
                </div>
              </div>
            </div>

            <div className="contact-info-footer">{slogan}</div>
          </section>

          <section className="contact-form-card">
            <div className="contact-form-heading">
              <span className="contact-small-title">SEND US A MESSAGE</span>

              <h2>Gửi tin nhắn</h2>

              <p>
                Hãy để lại thông tin, đội ngũ {siteName} sẽ hỗ trợ bạn.
              </p>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="contact-form-group">
                <label htmlFor="contact-name">Họ và tên</label>
                <input
                  id="contact-name"
                  type="text"
                  placeholder="Nhập họ và tên của bạn"
                  required
                />
              </div>

              <div className="contact-form-group">
                <label htmlFor="contact-email">Địa chỉ Email</label>
                <input
                  id="contact-email"
                  type="email"
                  placeholder="example@email.com"
                  required
                />
              </div>

              <div className="contact-form-group">
                <label htmlFor="contact-message">Nội dung tin nhắn</label>
                <textarea
                  id="contact-message"
                  rows="6"
                  placeholder="Bạn cần WatchStore hỗ trợ điều gì?"
                  required
                ></textarea>
              </div>

              <button type="submit" className="contact-submit">
                GỬI TIN NHẮN <span>→</span>
              </button>
            </form>

            <div className="contact-form-note">
              <span>✦</span> {siteName} luôn trân trọng mọi ý kiến của bạn.
            </div>
          </section>
        </div>
      </div>
    </main>
  );
}

export default Contact;
