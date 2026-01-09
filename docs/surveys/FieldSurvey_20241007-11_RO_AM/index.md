---
title: FieldSurvey_20241007-11_RO_AM
---

# FieldSurvey_20241007-11_RO_AM

- **Survey Date**: 07/10/2024 - 11/10/2024
- **Member**: IBAMA: 4 / JICA: 2 / JICA BR: 2 / Other: 3
- **Map**: 
![[FieldSurvey_20241007-11_RO_AM.png]]

---
## point Map
<div id="map"></div>

<link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

<style>
  #map {
    height: 450px;
    margin: 1rem 0;
  }
</style>

<script>
  // ===== このページ専用設定 =====
  const TARGET_SURVEY_ID = "FieldSurvey_20241007-11_RO_AM";

  // トップと同じ GeoJSON を使う
  const GEOJSON_URL = "../../assets/MORI_survey_github.geojson";

  // ===== 地図初期化 =====
  const map = L.map("map").setView([-9.0, -63.0], 6);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(map);

  function filterBySurveyId(geojson, surveyId) {
    const feats = (geojson && geojson.features) ? geojson.features : [];
    const filtered = feats.filter((f) => {
      const p = (f && f.properties) || {};
      return (p.title || "") === surveyId;
    });
    return { ...geojson, features: filtered };
  }

  fetch(GEOJSON_URL)
    .then((r) => {
      if (!r.ok) throw new Error("GeoJSON load failed: " + r.status);
      return r.json();
    })
    .then((data) => {
      const filtered = filterBySurveyId(data, TARGET_TITLE);

      const layer = L.geoJSON(filtered, {
        pointToLayer: function (feature, latlng) {
          return L.circleMarker(latlng, {
            radius: 7,
            fillColor: "#e41a1c",
            color: "#000",
            weight: 1,
            fillOpacity: 0.9,
          });
        },
        onEachFeature: (feature, layer) => {
          const p = feature.properties || {};
          let html = "";

          if (p.title) html += "<b>" + p.title + "</b><br>";

          if (p.survey_id) {
            const id = String(p.survey_id).trim();
            const href = "./" + encodeURIComponent(id) + "/"; // ★ md直置き想定のURL
            html += 'Survey ID: <a href="' + href + '">' + id + "</a><br>";
          }

          if (p.region) html += "Mesh: " + p.region + "<br>";
          if (p.survey_date) html += "Date: " + p.survey_date + "<br>";

          if (html) layer.bindPopup(html);
        },
      }).addTo(map);

      if (layer.getBounds().isValid()) {
        map.fitBounds(layer.getBounds(), { padding: [20, 20] });
      } else {
        console.warn("No points found for survey_id:", TARGET_TITLE);
      }
    })
    .catch((e) => console.error(e));
</script>
---

## Suevey id list
| ID | Mesh |
|--------|------|
| [HU-AM-2410-05Ref](./HU-AM-2410-05Ref) | S07W064 |
| [HU-AM-2410-06](./HU-AM-2410-06) | S07W064 |
| [HU-AM-2410-07Ref](./HU-AM-2410-07Ref) | S07W064 |
| [HU-AM-2410-08](./HU-AM-2410-08) | S07W064 |
| [HU-AM-2410-09](./HU-AM-2410-09) | S07W064 |
| [HU-AM-2410-10](./HU-AM-2410-10) | S07W064 |
| [HU-AM-2410-11](./HU-AM-2410-11) | S07W063 |
| [HU-AM-2410-12](./HU-AM-2410-12) | S07W063 |
| [HU-AM-2410-15](./HU-AM-2410-15) | S07W064 |
| [HU-AM-2410-18](./HU-AM-2410-18) | S07W064 |
| [HU-AM-2410-19](./HU-AM-2410-19) | S07W064 |
| [HU-AM-2410-20Ref](./HU-AM-2410-20Ref) | S07W064 |
| [PV-RO-2410-01Ref](./PV-RO-2410-01Ref) | S08W064 |
| [PV-RO-2410-02](./PV-RO-2410-02) | S09W065 |
| [PV-RO-2410-03](./PV-RO-2410-03) | S09W065 |
| [PV-RO-2410-08](./PV-RO-2410-08) | S08W064 |
