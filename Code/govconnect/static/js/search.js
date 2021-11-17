async function queryDB(searchTerm) {
    return (await fetch("/service/api/search/", { body: JSON.stringify({ search_term: searchTerm }), method: "POST" })).json();
}

if (window.location.pathname === '/account/') {
    // Select the input field and attach an event listener
    const search = document.querySelector('#searchField');
    const resultOutput = document.querySelector('#searchResults'); resultOutput.style.display = 'none';
    const recommendedServices = document.querySelector('#recommendedServices');

    let prevSearchTerm = '';
    search.addEventListener('keyup', async (e) => {
        const searchValue = e.target.value;
        if (searchValue.trim().length > 0) {
            if (prevSearchTerm.toLowerCase() !== searchValue.toLowerCase()) {
                recommendedServices.style.display = 'none';
                resultOutput.innerHTML = '';

                try {
                    await queryDB(searchValue).then((data) => {
                        console.log(data);
                        resultOutput.style.display = 'block';
                        if (data.length === 0) {
                            resultOutput.innerHTML = '<p>No results found</p>';
                        } else {
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
                } catch (e) {
                    console.log("Error:", e);
                }
            }
            prevSearchTerm = searchValue;
        } else {
            resultOutput.style.display = 'none';
            recommendedServices.style.display = 'block';
        }
    });
}
