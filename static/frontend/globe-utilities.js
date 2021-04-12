class Globe {
    constructor(allArticles) {
        // moved the class fields into constructor to better support older ios safari's

        // VALUES_FOR_STATIC_FILES is set inside index.html, not here
        this.activeIconImage = VALUES_FOR_STATIC_FILES.ACTIVE_ICON_IMAGE
        this.inactiveIconImage = VALUES_FOR_STATIC_FILES.INACTIVE_ICON_IMAGE
        this.zoomLevel = 2.5
        this.markerClickedFunction = null; // this will be set after the VueApp is created

        //== actual constructor stuff begins here ==

        this.initializeGlobe(); // sets this.globe
        this.initializeMarkers(allArticles); // sets this.allMarkers
        // display active markers for every article
        this.displayMarkersForArticles(allArticles, []);
    }

    initializeGlobe() {
        // equivalent to the documentation's initialize() function
        const globe = new WE.map("globe-div", {
            sky: true, // adds stars to background
        });
        //WE.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(globe);
        WE.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}').addTo(globe)

        globe.setZoom(this.zoomLevel);
        
        // Start a simple rotation animation
        // http://examples.webglearth.com/#animation
        var before = null;
        requestAnimationFrame(function animate(now) {

            // this line isn't in the documentation
            // I added it myself to change rotation speed depending on zoom level
            // suggested by Anthony Marx to make it easier to click markers when zoomed in
            // original rotation speed in documention example was hardcoded as 0.1
            // Math.min is used because otherwise the globe spins crazy fast when you zoom out too far
            const z = globe.getZoom();
            const rotationSpeed = Math.min( 
                0.1,
                1 / ( 2 * z * z )
            );

            var c = globe.getPosition();
            var elapsed = before? now - before: 0;
            before = now;
            globe.setCenter([c[0], c[1] - rotationSpeed*(elapsed/30)]);
            requestAnimationFrame(animate);
        });

        this.globe = globe;
    }

    // https://github.com/pointhi/leaflet-color-markers
    // create green active and grey inactive markers
    createMarker(locationName, coordinates, isActive, articleURL) {
        const iconURL = isActive ? this.activeIconImage : this.inactiveIconImage;
        
        const newMarker = WE.marker(coordinates, iconURL).bindPopup(locationName, 75);

        newMarker.element.onclick = () => {
            // close the popup 2.5 seconds after the marker is clicked
            setTimeout(() => newMarker.closePopup(), 2500);

            // needs to be set from outside, after the VueApp is created
            this.markerClickedFunction(articleURL, coordinates);
        }

        return newMarker;
    }

    // create markers for each location in each article
    // and place them in an object to be retrieved later
    initializeMarkers(allArticles) {
        // maps article url => markers for that url
        this.allMarkers = {};

        for (const article of allArticles) {
            this.allMarkers[ article.url ] = [];

            for (const locationName in article.locations) {
                const coordinates = article.locations[locationName];

                const newMarker = this.createMarker(locationName, coordinates, true, article.url);

                this.allMarkers[ article.url ].push(newMarker);
            }
        }
    }

    // remove all existing markers from the globe
    clearAllMarkers() {
        for (const url in this.allMarkers) {
            for (const marker of this.allMarkers[url]) {
                marker.removeFrom(this.globe);
            }
        }
    }

    displayMarkersForArticles(activeArticles, inactiveArticles) {
        this.clearAllMarkers();

        const displayMarkers = (articles, iconImage) => {
            for (const article of articles) {
                for (const marker of this.allMarkers[ article.url ]) {
                    // look at the html structure to understand this
                    marker.element.querySelector(".we-pm-icon")
                        .style.backgroundImage = `url("${iconImage}")`;

                    marker.addTo(this.globe);
                }
            }
        }

        // render inactive first, so active markers at same location will appear above them
        displayMarkers(inactiveArticles, this.inactiveIconImage);
        displayMarkers(activeArticles, this.activeIconImage);
    }

    moveTo(coordinates) {
        this.globe.setView(coordinates, this.zoomLevel);
    }
}
