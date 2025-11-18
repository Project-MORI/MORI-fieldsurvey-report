# MORI Field Survey Report

## Survey Map

<div id="map"></div>

<link
  rel="stylesheet"
  href="https://unpkg.com/leaflet/dist/leaflet.css"
/>
<link
  rel="stylesheet"
  href="https://unpkg.com/leaflet.markercluster/dist/MarkerCluster.css"
/>
<link
  rel="stylesheet"
  href="https://unpkg.com/leaflet.markercluster/dist/MarkerCluster.Default.css"
/>

<script>
  // トップページから見た GeoJSON の相対パス
  const geojsonUrl = "./assets/MORI_survey_github.geojson";

  // 適当な初期中心・ズーム（Amazon全体イメージ）
  const map = L.map("map").setView([-4.5, -62.0], 5);

  // 背景地図（OpenStreetMap）
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(map);

  // ---- 調査名ごとの色分け用 ----
  const titleColorMap = {};
  const colorPalette = [
    "#e41a1c", "#377eb8", "#4daf4a", "#984ea3",
    "#ff7f00", "#a65628", "#f781bf", "#999999"
  ];

  function getColorForTitle(title) {
    if (!title) {
      return "#3388ff"; // デフォルト色
    }
    if (!titleColorMap[title]) {
      const idx = Object.keys(titleColorMap).length % colorPalette.length;
      titleColorMap[title] = colorPalette[idx];
    }
    return titleColorMap[title];
  }

  // ---- マーカークラスタグループ ----
  const clusterGroup = L.markerClusterGroup();

  // GeoJSON 読み込み
  fetch(geojsonUrl)
    .then((response) => response.json())
    .then((data) => {
      const geojsonLayer = L.geoJSON(data, {
        // 各ポイントの見た目（circleMarker + titleごと色分け）
        pointToLayer: function (feature, latlng) {
          const props = feature.properties || {};
          const title = props.title || props.name || "";
          const color = getColorForTitle(title);

          return L.circleMarker(latlng, {
            radius: 6,
            fillColor: color,
            color: "#000000",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.9,
          });
        },

        // ポップアップ（IDをリンクにする）
        onEachFeature: function (feature, layer) {
          const p = feature.properties || {};
          const id = p.survey_id || p.id || "";
          const title = p.title || p.name || "";
          // まだGeoJSONにURL列がないので、暫定的に "#"
          const url = p.page_url || "#";

          let html = "";
          if (title) html += "<b>" + title + "</b><br>";

          if (id) {
            html += 'ID: <a href="' + url + '">' + id + "</a><br>";
          }

          // 他に表示したい属性があればここに追記
          // if (p.region) html += "Mesh: " + p.region + "<br>";

          if (html) {
            layer.bindPopup(html);
          }
        },
      });

      // GeoJSONレイヤーをクラスタグループに追加
      clusterGroup.addLayer(geojsonLayer);
      map.addLayer(clusterGroup);

      // すべての点が入るようにズーム調整
      try {
        map.fitBounds(clusterGroup.getBounds());
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
