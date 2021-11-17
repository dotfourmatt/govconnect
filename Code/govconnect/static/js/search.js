const boldResult = (text, searchTerm) => text.replace(RegExp(searchTerm, 'ig'), `<b>${searchTerm}</b>`);

if (window.location.pathname === '/account/') {
    // Select the input field and attach an event listener
    const search = document.querySelector('#searchField');
    const resultOutput = document.querySelector('#searchResults');
    const recommendedServices = document.querySelector('#recommendedServices');
    resultOutput.style.display = 'none';

    let prevSearchTerm = '';

    search.addEventListener('keyup', (e) => {
        const searchValue = e.target.value;

        if (searchValue.trim().length > 0) {
            if (prevSearchTerm.toLowerCase() !== searchValue.toLowerCase()) {
                recommendedServices.style.display = 'none';
                resultOutput.innerHTML = '';

                fetch("/service/api/search/", {
                    body: JSON.stringify({ search_term: searchValue }),
                    method: "POST"
                })
                    .then((res) => res.json())
                    .then((data) => {
                        resultOutput.style.display = 'block';

                        if (data.length === 0) {
                            resultOutput.innerHTML = '<p>No results found</p>';
                        } else {
                            //console.log("data", data);
                            //resultOutput.innerHTML += `<p>No Results: ${data.length}</p>`
                            data.forEach((service) => {
                                resultOutput.innerHTML += `
                                <div class="search_result">
                                    <div class="result_title">
                                        ${service.name} - ${service.category}
                                    </div>
                                    <div class="result_description">
                                        ${service.description}
                                    </div>
                                    <div class="more_info">
                                        For more information click <a href="/service/${service.state}/${service.name_slug}">here</a>.
                                    </div>
                                </div>
                                `;
                            });
                        }
                    });
            }
            prevSearchTerm = searchValue;
        } else {
            resultOutput.style.display = 'none';
            recommendedServices.style.display = 'block';
        }
    });
}
