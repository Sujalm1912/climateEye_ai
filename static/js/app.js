/**
 * ClimateEYE: Real-Time Environmental Dashboard, Dynamic City Search & AI Chatbot
 * Securely communicates with backend service layer for:
 * - Dynamic Forward Geocoding (Open-Meteo & Nominatim)
 * - Reverse-Geocoding & GPS
 * - Real-time Open-Meteo Weather
 * - Context-Aware AI Climate Assistant
 */

document.addEventListener('DOMContentLoaded', () => {
  // Global State
  window.climateBotContext = null;

  // Search Elements
  const inputSearch = document.getElementById('input-location-search');
  const btnClearSearch = document.getElementById('btn-clear-search');
  const btnExecuteSearch = document.getElementById('btn-execute-search');
  const searchDropdown = document.getElementById('search-dropdown-menu');

  // Dashboard Trigger & Alerts
  const btnUseLocation = document.getElementById('btn-use-location');
  const btnTestCoords = document.getElementById('btn-test-coords');
  const alertBanner = document.getElementById('alert-banner');
  const alertTitle = document.getElementById('alert-title');
  const alertMessage = document.getElementById('alert-message');
  const alertAction = document.getElementById('alert-action');

  // Containers
  const envEmptyState = document.getElementById('env-empty-state');
  const envSkeleton = document.getElementById('env-skeleton');
  const envDashboard = document.getElementById('env-dashboard');

  // Location Strip Fields
  const displayLocationName = document.getElementById('display-location-name');
  const displayLocationSub = document.getElementById('display-location-sub');
  const displayCoordLat = document.getElementById('display-coord-lat');
  const displayCoordLon = document.getElementById('display-coord-lon');
  const displayUpdatedTime = document.getElementById('display-updated-time');

  // Hero Weather Elements
  const heroWeatherIcon = document.getElementById('hero-weather-icon');
  const heroConditionText = document.getElementById('hero-condition-text');
  const heroCategoryText = document.getElementById('hero-category-text');
  const heroTempDisplay = document.getElementById('hero-temp-display');
  const heroFeelsLikeDisplay = document.getElementById('hero-feels-like-display');

  // 6 Metric Display Elements
  const valMetricTemp = document.getElementById('val-metric-temp');
  const unitMetricTemp = document.getElementById('unit-metric-temp');
  const valMetricFeels = document.getElementById('val-metric-feels');
  const unitMetricFeels = document.getElementById('unit-metric-feels');
  const subMetricFeels = document.getElementById('sub-metric-feels');
  const valMetricHumidity = document.getElementById('val-metric-humidity');
  const unitMetricHumidity = document.getElementById('unit-metric-humidity');
  const barMetricHumidity = document.getElementById('bar-metric-humidity');
  const valMetricCloud = document.getElementById('val-metric-cloud');
  const unitMetricCloud = document.getElementById('unit-metric-cloud');
  const barMetricCloud = document.getElementById('bar-metric-cloud');
  const valMetricRain = document.getElementById('val-metric-rain');
  const unitMetricRain = document.getElementById('unit-metric-rain');
  const valMetricWind = document.getElementById('val-metric-wind');
  const unitMetricWind = document.getElementById('unit-metric-wind');

  // Flow Step Indicators
  const stepPerm = document.getElementById('step-perm');
  const stepCoords = document.getElementById('step-coords');
  const stepBackend = document.getElementById('step-backend');
  const stepWeather = document.getElementById('step-weather');

  // Diagnostic inputs
  const inputLat = document.getElementById('input-test-lat');
  const inputLon = document.getElementById('input-test-lon');

  // Chatbot Elements
  const chatbotContextText = document.getElementById('chatbot-context-text');
  const chatbotMessages = document.getElementById('chatbot-messages');
  const inputChatbotMsg = document.getElementById('input-chatbot-msg');
  const formChatbot = document.getElementById('form-chatbot');

  // Leaflet Map instance
  let mapInstance = null;
  let mapMarker = null;

  // Search Debounce Timer
  let searchDebounceTimer = null;

  // Initialize or update interactive Leaflet map
  function updateMap(lat, lon, zoom = 11) {
    if (typeof L === 'undefined') return;

    const mapEl = document.getElementById('map-container');
    if (!mapEl) return;

    if (!mapInstance) {
      mapInstance = L.map('map-container', {
        zoomControl: true,
        attributionControl: true
      }).setView([lat, lon], zoom);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(mapInstance);
    } else {
      mapInstance.setView([lat, lon], zoom);
      setTimeout(() => { mapInstance.invalidateSize(); }, 200);
    }

    if (mapMarker) {
      mapMarker.setLatLng([lat, lon]);
    } else {
      mapMarker = L.marker([lat, lon]).addTo(mapInstance);
    }
  }

  // Format decimal to cardinal string (e.g. 23.0225° N)
  function formatCoordinate(val, isLat) {
    const num = parseFloat(val);
    if (isNaN(num)) return 'N/A';
    const direction = isLat ? (num >= 0 ? 'N' : 'S') : (num >= 0 ? 'E' : 'W');
    return `${Math.abs(num).toFixed(4)}° ${direction}`;
  }

  // SVG Icons based on Category
  const WEATHER_SVGS = {
    clear: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />`,
    cloudy: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 00-9.78 2.096A4.001 4.001 0 003 15z" />`,
    rain: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 100-6 3 3 0 000 6z" />`,
    drizzle: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 14v.01M12 14v.01M16 14v.01M9 17v.01M13 17v.01M7 20v.01M11 20v.01M15 20v.01" />`,
    thunderstorm: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />`,
    snow: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 2v20m10-10H2m17.07 7.07l-14.14-14.14m0 14.14L19.07 4.93" />`,
    fog: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 12h16M4 16h16" />`
  };

  function setWeatherIcon(category) {
    const iconContent = WEATHER_SVGS[category] || WEATHER_SVGS['cloudy'];
    heroWeatherIcon.innerHTML = iconContent;
  }

  // Flow State Indicators
  function resetFlowSteps() {
    [stepPerm, stepCoords, stepBackend, stepWeather].forEach(step => {
      step.classList.remove('active', 'completed');
    });
  }

  function setStepActive(stepEl) {
    stepEl.classList.remove('completed');
    stepEl.classList.add('active');
  }

  function setStepCompleted(stepEl) {
    stepEl.classList.remove('active');
    stepEl.classList.add('completed');
  }

  function hideError() {
    alertBanner.classList.remove('visible');
    alertAction.style.display = 'none';
  }

  function showError(title, message, recommendation = '') {
    alertBanner.classList.add('visible');
    alertTitle.textContent = title;
    alertMessage.textContent = message;

    if (recommendation) {
      alertAction.textContent = recommendation;
      alertAction.style.display = 'block';
    } else {
      alertAction.style.display = 'none';
    }
    alertBanner.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function setUiLoading(isLoading) {
    if (isLoading) {
      btnUseLocation.classList.add('loading');
      btnUseLocation.disabled = true;
      btnTestCoords.disabled = true;
      hideError();
      envEmptyState.style.display = 'none';
      envDashboard.classList.remove('visible');
      envSkeleton.classList.add('visible');
    } else {
      btnUseLocation.classList.remove('loading');
      btnUseLocation.disabled = false;
      btnTestCoords.disabled = false;
      envSkeleton.classList.remove('visible');
    }
  }

  // Coordinate Validation
  function validateCoordinates(lat, lon) {
    if (lat === null || lat === undefined || lon === null || lon === undefined || lat === '' || lon === '') {
      return { valid: false, error: 'Both latitude and longitude values are required.' };
    }
    const numLat = Number(lat);
    const numLon = Number(lon);

    if (isNaN(numLat) || isNaN(numLon)) {
      return { valid: false, error: 'Coordinates must be valid numbers.' };
    }
    if (numLat < -90 || numLat > 90) {
      return { valid: false, error: `Invalid latitude: ${numLat}. Must be between -90 and 90 degrees.` };
    }
    if (numLon < -180 || numLon > 180) {
      return { valid: false, error: `Invalid longitude: ${numLon}. Must be between -180 and 180 degrees.` };
    }
    return { valid: true, lat: numLat, lon: numLon };
  }

  /**
   * Fetch Environmental Climate Snapshot from Backend Service Layer
   */
  async function fetchEnvironmentalSnapshot(lat, lon, knownLocationName = null) {
    setStepActive(stepBackend);

    try {
      const response = await fetch('/api/climate-snapshot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ latitude: lat, longitude: lon })
      });

      const json = await response.json();

      if (!response.ok) {
        throw new Error(json.message || `Server error (${response.status})`);
      }

      setStepCompleted(stepBackend);
      setStepActive(stepWeather);

      // If user selected from search, use the specific resolved city label
      const locData = json.data.location;
      if (knownLocationName) {
        locData.readable_name = knownLocationName;
      }

      renderDashboard(locData, json.data.weather);
      updateChatbotContext(locData, json.data.weather);
      setStepCompleted(stepWeather);
    } catch (err) {
      stepBackend.classList.remove('active');
      stepWeather.classList.remove('active');
      envEmptyState.style.display = 'flex';
      showError(
        'Telemetry Retrieval Error',
        err.message || 'Failed to retrieve environmental telemetry from backend service.',
        'Tip: Check server status and coordinate ranges.'
      );
    } finally {
      setUiLoading(false);
    }
  }

  /**
   * Render Populated Environmental Dashboard
   */
  function renderDashboard(loc, weather) {
    envEmptyState.style.display = 'none';
    envSkeleton.classList.remove('visible');
    envDashboard.classList.add('visible');

    // Location Strip
    displayLocationName.textContent = loc.readable_name || `${loc.city || ''} ${loc.country || ''}`.trim() || 'Selected Location';
    displayLocationSub.textContent = loc.display_name || 'Observation Point';
    displayCoordLat.textContent = formatCoordinate(loc.latitude, true);
    displayCoordLon.textContent = formatCoordinate(loc.longitude, false);
    displayUpdatedTime.textContent = `Live ${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;

    // Atmospheric Hero Card
    heroConditionText.textContent = weather.weather_condition;
    heroCategoryText.textContent = `WMO Code ${weather.weather_code} • ${weather.source}`;
    heroTempDisplay.textContent = `${weather.temperature !== null ? weather.temperature : '--'}${weather.units.temperature}`;
    heroFeelsLikeDisplay.textContent = `Feels like ${weather.apparent_temperature !== null ? weather.apparent_temperature : '--'}${weather.units.apparent_temperature}`;
    setWeatherIcon(weather.weather_category);

    // Metric 1: Temperature
    valMetricTemp.textContent = weather.temperature !== null ? weather.temperature : '--';
    unitMetricTemp.textContent = weather.units.temperature;

    // Metric 2: Feels-Like / Apparent Temperature
    valMetricFeels.textContent = weather.apparent_temperature !== null ? weather.apparent_temperature : '--';
    unitMetricFeels.textContent = weather.units.apparent_temperature;
    if (weather.apparent_temperature > weather.temperature) {
      subMetricFeels.textContent = 'High heat index / humidity effect';
    } else if (weather.apparent_temperature < weather.temperature) {
      subMetricFeels.textContent = 'Wind chill factor active';
    } else {
      subMetricFeels.textContent = 'Thermal equilibrium with ambient';
    }

    // Metric 3: Relative Humidity
    valMetricHumidity.textContent = weather.relative_humidity !== null ? weather.relative_humidity : '--';
    unitMetricHumidity.textContent = weather.units.relative_humidity;
    barMetricHumidity.style.width = `${Math.min(100, Math.max(0, weather.relative_humidity || 0))}%`;

    // Metric 4: Cloud Cover
    valMetricCloud.textContent = weather.cloud_cover !== null ? weather.cloud_cover : '--';
    unitMetricCloud.textContent = weather.units.cloud_cover;
    barMetricCloud.style.width = `${Math.min(100, Math.max(0, weather.cloud_cover || 0))}%`;

    // Metric 5: Precipitation
    valMetricRain.textContent = weather.precipitation !== null ? weather.precipitation : '0.0';
    unitMetricRain.textContent = weather.units.precipitation;

    // Metric 6: Wind Speed
    valMetricWind.textContent = weather.wind_speed !== null ? weather.wind_speed : '--';
    unitMetricWind.textContent = weather.units.wind_speed;

    // Interactive Leaflet Map
    updateMap(loc.latitude, loc.longitude, 11);
  }

  /**
   * Synchronize Chatbot Context with current location & telemetry
   */
  function updateChatbotContext(loc, weather) {
    const locName = loc.readable_name || loc.city || 'Selected Location';
    window.climateBotContext = {
      location: locName,
      city: loc.city,
      state: loc.state,
      country: loc.country,
      latitude: loc.latitude,
      longitude: loc.longitude,
      weather: {
        condition: weather.weather_condition,
        temperature: weather.temperature,
        apparent_temperature: weather.apparent_temperature,
        relative_humidity: weather.relative_humidity,
        cloud_cover: weather.cloud_cover,
        precipitation: weather.precipitation,
        wind_speed: weather.wind_speed,
        units: weather.units
      }
    };

    // Update Context Tag Pill
    chatbotContextText.textContent = `Context: ${locName} (${weather.temperature}°C • ${weather.weather_condition})`;

    // Add updated introductory bot message
    addBotMessage(
      `Hello! I'm now synchronized with live telemetry for **${locName}**.\n` +
      `Current conditions: **${weather.temperature}°C** (feels like **${weather.apparent_temperature}°C**), ` +
      `**${weather.weather_condition}**, **${weather.relative_humidity}%** humidity, and **${weather.wind_speed} km/h** wind.\n\n` +
      `How can I assist you with this climate zone today?`
    );
  }

  function addUserMessage(text) {
    const msgEl = document.createElement('div');
    msgEl.className = 'chat-bubble chat-bubble-user';
    msgEl.textContent = text;
    chatbotMessages.appendChild(msgEl);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
  }

  function addBotMessage(markdownText) {
    const msgEl = document.createElement('div');
    msgEl.className = 'chat-bubble chat-bubble-bot';
    // Format simple bold markdown
    let formatted = markdownText
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n/g, '<br/>');
    msgEl.innerHTML = formatted;
    chatbotMessages.appendChild(msgEl);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
  }

  async function handleChatbotSubmit(query) {
    if (!query || !query.trim()) return;
    const text = query.trim();
    addUserMessage(text);
    inputChatbotMsg.value = '';

    if (!window.climateBotContext) {
      addBotMessage("Please select or search a location first so I can analyze its live climate conditions.");
      return;
    }

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          context: window.climateBotContext
        })
      });
      const data = await res.json();
      if (data.status === 'success') {
        addBotMessage(data.reply);
      } else {
        addBotMessage("Sorry, I encountered an issue analyzing the telemetry.");
      }
    } catch (err) {
      addBotMessage("Connection error communicating with the climate assistant.");
    }
  }

  // Chatbot Event Listeners
  formChatbot.addEventListener('submit', (e) => {
    e.preventDefault();
    handleChatbotSubmit(inputChatbotMsg.value);
  });

  document.querySelectorAll('.btn-prompt-chip').forEach(btn => {
    btn.addEventListener('click', () => {
      handleChatbotSubmit(btn.getAttribute('data-query'));
    });
  });

  /**
   * Location Search & Autocomplete
   */
  async function searchCities(query) {
    if (!query || query.trim().length < 2) {
      searchDropdown.style.display = 'none';
      searchDropdown.innerHTML = '';
      return;
    }

    try {
      const res = await fetch(`/api/search-locations?q=${encodeURIComponent(query.trim())}&limit=5`);
      const data = await res.json();

      if (data.status === 'success' && data.results && data.results.length > 0) {
        renderSearchDropdown(data.results);
      } else {
        searchDropdown.innerHTML = '<li class="search-dropdown-item"><span class="dropdown-item-sub">No locations found. Try another city name.</span></li>';
        searchDropdown.style.display = 'block';
      }
    } catch (err) {
      console.error('Search error:', err);
    }
  }

  function renderSearchDropdown(results) {
    searchDropdown.innerHTML = '';
    results.forEach(item => {
      const li = document.createElement('li');
      li.className = 'search-dropdown-item';
      li.setAttribute('role', 'option');
      li.innerHTML = `
        <div>
          <div class="dropdown-item-title">${item.readable_name}</div>
          <div class="dropdown-item-sub">${item.country || 'Global Location'} &bull; ${item.provider || 'Geocoding'}</div>
        </div>
        <div class="dropdown-item-coords">${item.latitude.toFixed(3)}, ${item.longitude.toFixed(3)}</div>
      `;

      li.addEventListener('click', () => {
        selectSearchResult(item);
      });

      searchDropdown.appendChild(li);
    });
    searchDropdown.style.display = 'block';
  }

  function selectSearchResult(item) {
    inputSearch.value = item.readable_name;
    btnClearSearch.style.display = 'block';
    searchDropdown.style.display = 'none';

    if (inputLat && inputLon) {
      inputLat.value = item.latitude.toFixed(4);
      inputLon.value = item.longitude.toFixed(4);
    }

    resetFlowSteps();
    setStepCompleted(stepPerm);
    setStepCompleted(stepCoords);
    setUiLoading(true);

    fetchEnvironmentalSnapshot(item.latitude, item.longitude, item.readable_name);
  }

  // Search Input Handlers
  inputSearch.addEventListener('input', (e) => {
    const val = e.target.value;
    btnClearSearch.style.display = val.length > 0 ? 'block' : 'none';

    clearTimeout(searchDebounceTimer);
    searchDebounceTimer = setTimeout(() => {
      searchCities(val);
    }, 280);
  });

  inputSearch.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      executeDirectSearch();
    }
  });

  btnExecuteSearch.addEventListener('click', executeDirectSearch);

  async function executeDirectSearch() {
    const q = inputSearch.value.trim();
    if (!q) return;

    searchDropdown.style.display = 'none';
    setUiLoading(true);

    try {
      const res = await fetch(`/api/search-locations?q=${encodeURIComponent(q)}&limit=1`);
      const data = await res.json();
      if (data.status === 'success' && data.results && data.results.length > 0) {
        selectSearchResult(data.results[0]);
      } else {
        setUiLoading(false);
        showError('Location Not Found', `Could not find coordinates for "${q}". Please check the spelling or try another city.`);
      }
    } catch (err) {
      setUiLoading(false);
      showError('Search Error', 'Failed to communicate with the geocoding service.');
    }
  }

  btnClearSearch.addEventListener('click', () => {
    inputSearch.value = '';
    btnClearSearch.style.display = 'none';
    searchDropdown.style.display = 'none';
  });

  // Close dropdown when clicking outside
  document.addEventListener('click', (e) => {
    if (!inputSearch.contains(e.target) && !searchDropdown.contains(e.target)) {
      searchDropdown.style.display = 'none';
    }
  });

  /**
   * Main Handler: Request Browser Geolocation
   */
  function handleUseMyLocation() {
    hideError();
    resetFlowSteps();
    setUiLoading(true);

    if (!('geolocation' in navigator)) {
      setUiLoading(false);
      showError(
        'Geolocation Unsupported',
        'The Geolocation API is not supported by your current browser environment.',
        'Try searching for your city in the search bar above.'
      );
      return;
    }

    setStepActive(stepPerm);

    const geoOptions = {
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 0
    };

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        setStepCompleted(stepPerm);
        setStepActive(stepCoords);

        const lat = position.coords.latitude;
        const lon = position.coords.longitude;

        setStepCompleted(stepCoords);

        if (inputLat && inputLon) {
          inputLat.value = lat.toFixed(4);
          inputLon.value = lon.toFixed(4);
        }

        const validation = validateCoordinates(lat, lon);
        if (!validation.valid) {
          setUiLoading(false);
          showError('Invalid Coordinates', validation.error);
          return;
        }

        await fetchEnvironmentalSnapshot(lat, lon);
      },
      (geoError) => {
        setUiLoading(false);
        resetFlowSteps();

        switch (geoError.code) {
          case geoError.PERMISSION_DENIED:
            showError(
              'Permission Denied (Code 1)',
              'You denied location access. Browser permission is needed to monitor your local climate zone.',
              'Click the lock/tune icon in your browser URL bar to grant location permission, or search your city above.'
            );
            break;
          case geoError.POSITION_UNAVAILABLE:
            showError(
              'Location Unavailable (Code 2)',
              'Position information could not be determined by your network or device GPS.',
              'Use the search bar above to search for your city.'
            );
            break;
          case geoError.TIMEOUT:
            showError(
              'Location Request Timed Out (Code 3)',
              'The request to get user location timed out after 10 seconds.',
              'Check your connection or search your city above.'
            );
            break;
          default:
            showError('Location Error', geoError.message || 'An unknown error occurred while retrieving location coordinates.');
            break;
        }
      },
      geoOptions
    );
  }

  /**
   * Manual Coordinates / Presets Handler
   */
  async function handleFetchCoordinates(latInput, lonInput, locationLabel = null) {
    hideError();
    const latRaw = latInput !== undefined ? latInput : inputLat.value.trim();
    const lonRaw = lonInput !== undefined ? lonInput : inputLon.value.trim();

    const validation = validateCoordinates(latRaw, lonRaw);
    if (!validation.valid) {
      showError('Invalid Coordinates', validation.error);
      return;
    }

    resetFlowSteps();
    setStepCompleted(stepPerm);
    setStepCompleted(stepCoords);

    setUiLoading(true);
    await fetchEnvironmentalSnapshot(validation.lat, validation.lon, locationLabel);
  }

  // Presets click events
  document.querySelectorAll('.btn-preset').forEach(btn => {
    btn.addEventListener('click', () => {
      const lat = btn.getAttribute('data-lat');
      const lon = btn.getAttribute('data-lon');
      const label = btn.textContent.trim().replace('📍 ', '');

      if (lat && lon) {
        inputLat.value = lat;
        inputLon.value = lon;
        inputSearch.value = label;
        btnClearSearch.style.display = 'block';
        handleFetchCoordinates(lat, lon, label);
      }
    });
  });

  // Event Listeners
  btnUseLocation.addEventListener('click', handleUseMyLocation);
  btnTestCoords.addEventListener('click', () => handleFetchCoordinates());

  // Auto-load Ahmedabad on initial startup for seamless demonstration
  const ahmedabadBtn = document.getElementById('btn-preset-ahmedabad');
  if (ahmedabadBtn) {
    setTimeout(() => {
      handleFetchCoordinates(23.0258, 72.5873, 'Ahmedabad, Gujarat, India');
    }, 300);
  }
});
