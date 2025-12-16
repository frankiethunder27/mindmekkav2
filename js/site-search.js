// Blocs Search V2.0

(function()
{
    if (!siteRelativeURLPath) // Global Variable Not Available
    {
        var scriptUrl = new URL(document.currentScript.src);
        var parentDirectory = scriptUrl.pathname.substring(0, scriptUrl.pathname.lastIndexOf("/js/")+1);
        siteRelativeURLPath = scriptUrl.origin + parentDirectory;
    }

    var dataPath = siteRelativeURLPath+'js/site-search-data.json?'+Math.random();

    fetch(dataPath)
        .then(response => response.json())
        .then(data => {
            blocsSearchSearchData = data;
        });

    var searchField = document.querySelector('[data-blocs-search="true"]');

    if (searchField)
    {
        searchField.addEventListener('keyup', function(event) {filterSearchResults(searchField);});
    }
})();


// Filter Search Results
function filterSearchResults(searchFieldElement)
{
    var searchQuery = searchFieldElement.value;
    document.querySelector('.blocs-search-results').innerHTML = '';

    if (searchQuery.length > 0) // Has Search value
    {
        searchFieldElement.parentElement.classList.remove('hide-search-results');
        var filteredArray = [];

        for (var i = 0; i < blocsSearchSearchData.length; i++) {
            var linkObj = blocsSearchSearchData[i];
            var linkTitle = linkObj["title"];
            var targetSearchData = linkTitle + ', ' + linkObj["keywords"];

            if (targetSearchData.toLowerCase().indexOf(searchQuery.toLowerCase()) != -1 && linkTitle != document.title) // Found Match
            {
                if (filteredArray.indexOf(linkObj) == -1) // Not in filtered array
                {
                    filteredArray.push(linkObj);
                }
            }
        }

        var titleColorClass = 'text-dark';
        var infoColorClass = 'text-muted';

        if (searchFieldElement.parentElement.classList.contains('dark-results-theme')) // Dark Results Theme
        {
            titleColorClass = 'text-white';
            infoColorClass = 'text-secondary';
        }

        if (filteredArray.length > 0) // Has Results
        {
            for (var i = 0; i < filteredArray.length; i++) // Loop Matches
            {
                var matchedItem = filteredArray[i];
                var pageURL = matchedItem.url;
                var description = matchedItem.description;

                if (!pageURL.startsWith("http"))
                {
                    pageURL = siteRelativeURLPath + pageURL;
                }

                if (typeof description == 'undefined')
                {
                    description = '';
                }

                document.querySelector('.blocs-search-results').insertAdjacentHTML('beforeend', '<a class="dropdown-item ' + titleColorClass + '" href="' + pageURL + '">' + matchedItem.title + '<br><span class="'+infoColorClass+'">'+description+'</span></a>');
            }
        }
        else
        {
            var noResultsText = document.querySelector('[data-blocs-search="true"]').getAttribute('data-no-results');
            document.querySelector('.blocs-search-results').insertAdjacentHTML('beforeend', '<span class="dropdown-item ' + titleColorClass + '">' + noResultsText + '</span>');
        }

        document.querySelector('.blocs-search-results').classList.add('show'); // Show Results Dropdown
    }
    else // No Results
    {
        document.querySelector('.blocs-search-results').classList.remove('show'); // Hide Results Dropdown
        searchFieldElement.parentElement.classList.add('hide-search-results');
    }
}

// Globar Vars
var siteRelativeURLPath;
var blocsSearchSearchData;