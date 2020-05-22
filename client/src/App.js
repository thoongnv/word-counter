import React, { useState } from 'react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Legend } from 'recharts';
import 'normalize.css';
import './App.css';

const Histogram = ({ histogramData, histogramOptions, updateHistogramOptions }) => {
    // Display component with http://recharts.org/
    function handleChangeWordOptions(e) {
        histogramOptions.limit = e.target.value;
        updateHistogramOptions(histogramOptions);
    }

    function handleChangeOrderOptions(e) {
        histogramOptions.order = e.target.value;
        updateHistogramOptions(histogramOptions);
    }

    return (
        <div className="Histogram">
            <div className="Filter">
                <label htmlFor="words">Number of words </label>
                <select value={histogramOptions.limit} onChange={handleChangeWordOptions}>
                    { histogramOptions.filterWordOptions.map(({value, label}, index) => <option key={index} value={value}>{label}</option>) }
                </select>
                <label htmlFor="sorting">Frequency sorting </label>
                <select value={histogramOptions.order} onChange={handleChangeOrderOptions}>
                    { histogramOptions.filterOrderOptions.map(({value, label}, index) => <option key={index} value={value}>{label}</option>) }
                </select>
            </div>
            <div className="Recharts">
                <ResponsiveContainer width="90%" height={550}>
                    <BarChart data={histogramData} margin={{top: 10}}>
                        <XAxis dataKey="name" height={100} interval={0} angle={-90} textAnchor="end" />
                        <YAxis dataKey="frequency" />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="frequency" fill="#8884d8" />
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    )
}

function App() {
    // Main application component
    const [websiteUrl, setWebsiteUrl] = useState('');
    const [statisticId, setStatisticId] = useState(0);
    const [disabledBtn, setDisabledBtn] = useState(false);
    const [hasError, setHasError] = useState(false);
    const [infoMessage, setInfoMessage] = useState('');
    const [recentWebsites, setRecentWebsites] = useState([]);
    const [histogramData, setHistogramData] = useState([]);
    const [histogramOptions, setHistogramOptions] = useState({
        // default filter first 100 words order by decreasing frequency
        order: '-frequency',
        offset: 0,
        limit: 100,
        filterWordOptions: [],
        filterOrderOptions: [
            {label: 'Ascending', value: '+frequency'},
            {label: 'Descending', value: '-frequency'},
        ],
    });

    function getAPIUrl(path) {
        return process.env.REACT_APP_SERVER_URL + '/' + path.replace(/^\//, "");
    }

    function parseHistogramOptions(options) {
        return '?order=' + options.order + '&offset=' + options.offset + '&limit=' + options.limit;
    }

    function updateHistogramOptions(options, recentStatisticId=undefined) {
        // refetch the statistic via GET
        fetchStatisticData(recentStatisticId ? recentStatisticId : statisticId, options);
    }

    function handleRequestError(error) {
        setHasError(true);
        setHistogramData([]);
        setDisabledBtn(false);
        // catch the error
        if (error.json) {
            error.json().then(error => {
                setInfoMessage(error.message);
            }).catch(() => {
                setInfoMessage(error.statusText);
            })
        } else {
            setInfoMessage('Failed to fetch the statistics');
        }
    }

    function handleKeyPress(e) {
        if(e.key === 'Enter' && !disabledBtn){
            handleCalculateWords(e);
        }
    }

    function handleChangeWebsiteUrl(e) {
        setWebsiteUrl(e.target.value);
        setHasError(false);
        setInfoMessage('');
        // reset filter options
        histogramOptions.order = '-frequency';
        histogramOptions.offset = 0;
        histogramOptions.limit = 100;
        setHistogramOptions(histogramOptions);
    }

    function fetchStatisticData(statisticId, options) {
        // get word counter statistics
        let getUrl = getAPIUrl('/v1/statistics/') + statisticId + parseHistogramOptions(options);
        fetch(getUrl).then(response => {
            if (!response.ok) {
                throw response;
            }
            return response.json();
        }).then(data => {
            let words = data.words;
            let totalWords = (words && words.total) || 0;
            // build filter options, temporary sizes: 20, 100, All
            options.filterWordOptions = [];
            if (totalWords > 100) {
                options.filterWordOptions.push(
                    {label: 20, value: 20},
                    {label: 100, value: 100},
                    {label: 'All', value: 'undefined'},
                )
            } else if (totalWords > 20) {
                options.filterWordOptions.push(
                    {label: 20, value: 20},
                    {label: 'All', value: 'undefined'},
                )
                if (options.limit === 100) {
                    options.limit = 'undefined';
                }
            } else {
                options.filterWordOptions.push(
                    {label: 'All', value: 'undefined'},
                )
            }

            // save recent websites
            let foundIndex = recentWebsites.findIndex(website => website.statisticId === statisticId);
            let recentWebsiteUrl = undefined;
            if (foundIndex > -1) {
                recentWebsiteUrl = recentWebsites[foundIndex].websiteUrl;
                recentWebsites.splice(foundIndex, 1);
            } else {
                // keep most 5 recent websites
                if (recentWebsites.length >= 5) {
                    recentWebsites.pop();
                }
            }
            if (!recentWebsiteUrl) {
                recentWebsiteUrl = websiteUrl;
            }
            recentWebsites.unshift({
                websiteUrl: recentWebsiteUrl,
                statisticId: statisticId,
            })
            setRecentWebsites(recentWebsites);
            setWebsiteUrl(recentWebsiteUrl);
            setStatisticId(statisticId);
            setHistogramData((words && words.data) || []);
            setHistogramOptions(options);
            setHasError(false);
            setDisabledBtn(false);
            setInfoMessage('Found total <strong>' + totalWords + '</strong> words on ' + recentWebsiteUrl);
        }).catch(error => {
            handleRequestError(error);
        })
    }

    function handleClickRecentWebsite(e) {
        updateHistogramOptions(histogramOptions, parseInt(e.target.getAttribute('statistic_id')));
    }

    function handleCalculateWords(e) {
        // First create statistics via POST request, then retrieve the result via GET
        e.preventDefault();
        setDisabledBtn(true);
        fetch(getAPIUrl('/v1/statistics'), {
            method: 'POST',
            headers: {
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({website_url: websiteUrl, check_existing: true})
        }).then(response => {
            if (!response.ok) {
                throw response;
            }
            return response.json();
        }).then(data => {
            fetchStatisticData(data.id, histogramOptions);
        }).catch(error => {
            handleRequestError(error);
        })
    }

    return (
        <div className="App">
            <h2>Welcome to word counting website!</h2>

            { recentWebsites.length ?
                <div className="Recent">
                    <span htmlFor="recent">Recently websites</span><br/>
                    { recentWebsites.map(({websiteUrl, statisticId}) => <span className="button" onClick={handleClickRecentWebsite} key={statisticId} statistic_id={statisticId}>{websiteUrl}</span>) }
                </div>
            : null }

            <div className="Input">
                <input type="text" name="websiteUrl" value={websiteUrl} onChange={handleChangeWebsiteUrl} onKeyPress={handleKeyPress} placeholder="Enter the website URL"></input>
                <button type="button" disabled={disabledBtn} onClick={handleCalculateWords}>Calculate words</button>
            </div>

            { infoMessage.length ?
                <div className={"Info " + (hasError ? "Error" : "Success")}>
                    <span dangerouslySetInnerHTML={{ __html: infoMessage }} />
                </div>
            : null }

            { histogramData.length ?
                <Histogram
                    histogramData={histogramData}
                    histogramOptions={histogramOptions}
                    updateHistogramOptions={updateHistogramOptions} />
            : null }
        </div>
    )
}

export default App;
