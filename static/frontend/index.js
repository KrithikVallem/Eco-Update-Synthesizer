document.addEventListener("DOMContentLoaded", function() {
    // anything created outside of the Vue app is ALL_UPPERCASE

    // VALUES_FOR_STATIC_FILES is set inside index.html, not here
    const ALL_ARTICLES = VALUES_FOR_STATIC_FILES.ALL_ARTICLES;

    const VueApp = new Vue({
        el: "#app",
    
        // using [[ ]] as the Vue delimiters to avoid potential future conflicts with Jinja2 in Flask templates
        delimiters: ["[[", "]]"],
    
        data: {
            allArticles: ALL_ARTICLES,
            globe: new Globe(ALL_ARTICLES),
            articles: ALL_ARTICLES,
            searchQuery: "",
        },
    
        watch: {
            searchQuery: function(newSearchQuery) {
                // empty search means return everything
                if (newSearchQuery === "") {
                    this.articles = ALL_ARTICLES;
                } 
                else {
                    const isQueryInText = (query, text) => text.toLowerCase().includes( query.toLowerCase() );
                    const searchResults = ALL_ARTICLES.filter(a => isQueryInText(newSearchQuery, a.text));
                    this.articles = searchResults;
                }

                this.globe.displayMarkersForArticles(this.articles, []);
            }
        },

        methods: {
            // get the first few words of an article's text, and add ... at the end
            // also remove the headline if its the first few words of the text
            getInitialWords(text, headline) {
                return text.replace(headline, "").split(" ").slice(0, 25).join(" ") + "...";
            },

            articleClickedFunction(clickedArticleObj) {
                const nonClickedArticles = this.articles.filter(a => a.url !== clickedArticleObj.url);
                this.globe.displayMarkersForArticles([clickedArticleObj], nonClickedArticles);

                // get first location in clicked article's locations
                // and recenter globe to it
                for (const locationName in clickedArticleObj.locations) {
                    const coordinates = clickedArticleObj.locations[locationName];
                    this.globe.moveTo(coordinates);
                    break;
                }
            },
        },

        // when this Vue Instance is first mounted to the DOM
        mounted() {
            this.globe.markerClickedFunction = (clickedMarkersArticleURL, clickedMarkerCoordinates) => {
                const articlesContainer = document.querySelector("#articles-container");
                const allArticleCards = document.querySelectorAll(".article-card");

                // the ref attr for each article card in the html is set to its article.url
                const articleCard = this.$refs[ clickedMarkersArticleURL ][0];
                const articleCardImage = articleCard.querySelector("img");

                // scroll the clicked marker's article card to the top of the articles container
                //articlesContainer.scrollTop = articleCard.offsetTop;
                articleCardImage.scrollIntoView({behavior: "smooth", block: "center"});

                // collapse all non-collapsed article cards
                for (const card of allArticleCards) {
                    if (card.classList.contains("not-collapsed")) {
                        card.click();
                    }
                }
                // then open the clicked marker's article card
                articleCard.click();
                // and recenter globe to the clicked marker (because articleClickedFunction will move it the the first location of the clicked marker's article)
                this.globe.moveTo(clickedMarkerCoordinates)

                // add a temporary border to the clicked marker's article card that slowly fades away to draw attention
                articleCard.style.border = "5px solid var(--theme-green)";
                for (let i = 0; i <= 1; i += 0.05) {
                    setTimeout(() => {
                        // this should be same as --theme-green, but I can't set the transparency separatly
                        articleCard.style.border = `5px dashed rgba(40,167,69, ${1-i}`;
                    }, 1500*i);
                }
            }
        }
    });
});

