
const Setting = require("../models/Setting");

const DEFAULT_SETTINGS = {
  key: "website",
  siteName: "WatchStore",
  footerDescription:
    "Cửa hàng đồng hồ chính hãng với nhiều mẫu mã hiện đại, phù hợp cho mọi phong cách.",
  logoUrl: "",
  contactEmail: "support@watchstore.com",
  contactPhone: "+84 123 456 789",
  contactAddress: "TP. Hồ Chí Minh",
  workingHours: "Thứ 2 – Thứ 7 | 08:00 – 21:00",
  contactSlogan: "YOUR TIME, YOUR STYLE.",
  facebookUrl: "",
  instagramUrl: "",
  tiktokUrl: "",
};

const getOrCreateSettings = async () => {
  let settings = await Setting.findOne({ key: "website" });

  if (!settings) {
    settings = await Setting.create(DEFAULT_SETTINGS);
  }

  return settings;
};

const getSettings = async (req, res) => {
  try {
    const settings = await getOrCreateSettings();
    res.json(settings);
  } catch (error) {
    console.error("Get settings failed:", error);
    res.status(500).json({ message: "Get settings failed" });
  }
};

const updateSettings = async (req, res) => {
  try {
    const payload = {
      siteName: (req.body.siteName || "").trim(),
      footerDescription: (req.body.footerDescription || "").trim(),
      logoUrl: (req.body.logoUrl || "").trim(),
      contactEmail: (req.body.contactEmail || "").trim(),
      contactPhone: (req.body.contactPhone || "").trim(),
      contactAddress: (req.body.contactAddress || "").trim(),
      workingHours: (req.body.workingHours || "").trim(),
      contactSlogan: (req.body.contactSlogan || "").trim(),
      facebookUrl: (req.body.facebookUrl || "").trim(),
      instagramUrl: (req.body.instagramUrl || "").trim(),
      tiktokUrl: (req.body.tiktokUrl || "").trim(),
    };

    const settings = await Setting.findOneAndUpdate(
      { key: "website" },
      { $set: { ...payload, key: "website" } },
      { upsert: true, new: true, setDefaultsOnInsert: true },
    );

    res.json(settings);
  } catch (error) {
    console.error("Update settings failed:", error);
    res.status(500).json({ message: "Update settings failed" });
  }
};

module.exports = {
  getSettings,
  updateSettings,
};
