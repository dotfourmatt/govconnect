async function queryDB(searchTerm) {
    return (await fetch("/service/api/search/", { body: JSON.stringify({ search_term: searchTerm }), method: "POST" })).json();
}

const debounce = (callback, delay) => {
    let timeout;
    return function (...args) {
        if (timeout) {
            clearTimeout(timeout);
        }
        timeout = setTimeout(() => {
            callback(...args);
        }, delay);
    };
};

const boldSearchTerm = (serviceName, searchTerm) => serviceName.replace(RegExp(searchTerm, 'ig'), `<b>${searchTerm}</b>`);

if (window.location.pathname === '/account/') {
    // Select the input field and attach an event listener
    const searchDiv = document.getElementById('search');
    const search = document.getElementById('searchField');
    const resultOutput = document.getElementById('searchResults');
    resultOutput.style.display = 'none';
    const recommendedServices = document.getElementById('recommendedServices');

    let prevSearchTerm = '';
    let timeout = null;
    search.addEventListener('keyup', debounce(async (e) => {
        const searchValue = e.target.value;
        if (searchValue.trim().length > 0) {
            if (prevSearchTerm.toLowerCase() !== searchValue.toLowerCase()) {
                recommendedServices.style.display = 'none';
                resultOutput.innerHTML = '';

                try {
                    await queryDB(searchValue).then((data) => {
                        resultOutput.style.display = 'block';
                        if (data.length === 0) {
                            resultOutput.innerHTML = '<p>No results found</p>';
                        } else {
                            html = '';
                            data.forEach((service) => {
                                html += `
                                    <div class="search_result">
                                        <div class="result_title">
                                            ${boldSearchTerm(service.name, searchValue)}
                                        </div>
                                        <div class="result_description">
                                            ${service.description}
                                        </div>
                                        <div class="more_info">
                                            For more information click <a href="/service/${service.state.toLowerCase()}/${service.name_slug}">here</a>.
                                        </div>
                                    </div>
                                    `;
                            });
                            resultOutput.innerHTML = html;
                        }
                    });
                    searchDiv.scrollIntoView({ behavior: 'smooth' });
                } catch (e) {
                    console.log("Error:", e);
                }
            }
            prevSearchTerm = searchValue;
        } else {
            resultOutput.style.display = 'none';
            recommendedServices.style.display = 'block';
        }
    }, 500));
}
