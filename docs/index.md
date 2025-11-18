# MORI Field Survey Report

## Survey Map

<div id="map"></div>

<link
  rel="stylesheet"
  href="https://unpkg.com/leaflet/dist/leaflet.css"
/>
<style>
  #map {
    height: 600px;
    margin-top: 1rem;
    margin-bottom: 1rem;
  }
</style>

<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
<script>
  // トップページから見た GeoJSON の相対パス
  const geojsonUrl = "./assets/MORI_survey_github.geojson";

  const map = L.map("map").setView([-4.5, -62.0], 5); // 適当な初期中心・ズーム

  // 背景地図（OpenStreetMap）
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(map);

  // GeoJSON 読み込み
  fetch(geojsonUrl)
    .then((response) => response.json())
    .then((data) => {
      const layer = L.geoJSON(data, {
        onEachFeature: function (feature, layer) {
          const p = feature.properties || {};
          const id = p.survey_id || p.id || "";
          const title = p.title || p.name || "";
          const url = p.page_url || ""; // あればページへのリンクに使う

          let html = "";
          if (title) html += "<b>" + title + "</b><br>";
          if (id) html += "ID: " + id + "<br>";
          if (url) html += '<a href="' + url + '">Open survey page</a>';

          if (html) layer.bindPopup(html);
        },
      }).addTo(map);

      // すべての点が入るようにズーム調整
      try {
        map.fitBounds(layer.getBounds());
      } catch (e) {
        console.warn("fitBounds failed:", e);
      }
    })
    .catch((err) => {
      console.error("Failed to load GeoJSON:", err);
    });
</script>


## 調査名の一覧
<!-- BEGIN: AUTO_SURVEY_LIST -->
<ul>
  <li><a href="surveys/FieldSurvey_20211018-19_RO/">FieldSurvey_20211018-19_RO</a></li>
  <li><a href="surveys/FieldSurvey_20220214-21_PA/">FieldSurvey_20220214-21_PA</a></li>
  <li><a href="surveys/FieldSurvey_20220919-23_RO/">FieldSurvey_20220919-23_RO</a></li>
  <li><a href="surveys/FieldSurvey_20230525-0601_RO_AC/">FieldSurvey_20230525-0601_RO_AC</a></li>
  <li><a href="surveys/FIeldSurvey_20231008-14_PA/">FIeldSurvey_20231008-14_PA</a></li>
  <li><a href="surveys/FieldSurvey_20240205-06_PA/">FieldSurvey_20240205-06_PA</a></li>
  <li><a href="surveys/FieldSurvey_20240318-21_PA/">FieldSurvey_20240318-21_PA</a></li>
  <li><a href="surveys/FieldSurvey_20240610-14_PA/">FieldSurvey_20240610-14_PA</a></li>
  <li><a href="surveys/FieldSurvey_20241007-11_RO_AM/">FieldSurvey_20241007-11_RO_AM</a></li>
  <li><a href="surveys/FieldSurvey_20241023-27_PA/">FieldSurvey_20241023-27_PA</a></li>
  <li><a href="surveys/FieldSurvey_20250309-15_RO_AC/">FieldSurvey_20250309-15_RO_AC</a></li>
  <li><a href="surveys/FieldSurvey_20251006-16_PA/">FieldSurvey_20251006-16_PA</a></li>
  <li><a href="surveys/MORI2_TestSurvey_20250531-0608_RO_AM/">MORI2_TestSurvey_20250531-0608_RO_AM</a></li>
</ul>
<!-- END: AUTO_SURVEY_LIST -->
