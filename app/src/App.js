import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import './App.css';

function App() {
    const [websiteUrl, setWebsiteUrl] = useState('');
    const [disabledBtn, setDisabledBtn] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const [histogramData, setHistogramData] = useState([]);

    function handleKeyPress(e) {
        if(e.key === 'Enter' && !disabledBtn){
            handleCalculateWords(e);
        }
    }

    function handleCalculateWords(e) {
        e.preventDefault();
        setDisabledBtn(true);
        fetch('/v1/statistics', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({website_url: websiteUrl})
        }).then(response => {
            if (!response.ok) {
                throw response;
            }
            return response.json();
        }).then(data => {
            // get word counter statistics
            let getUrl = '/v1/statistics/' + data.id + '?order=-frequency&offset=0&limit=100';
            fetch(getUrl).then(response => {
                if (!response.ok) {
                    throw response;
                }
                return response.json();
            }).then(data => {
                setHistogramData((data.words && data.words.data) || []);
                setErrorMessage('');
                setDisabledBtn(false);
            })
        }).catch(error => {
            error.json().then(error => {
                setHistogramData([]);
                setErrorMessage(error.message);
                setDisabledBtn(false);
            })
        })
    }

    function handleChangeWebsiteUrl(e) {
        setWebsiteUrl(e.target.value);
        setErrorMessage('')
    }

    return (
        <div className="App">
            <div className="Input">
                <input type="text" value={websiteUrl} onChange={handleChangeWebsiteUrl} onKeyPress={handleKeyPress} placeholder="Enter the website URL"/>
                <button type="button" disabled={disabledBtn} onClick={handleCalculateWords}>Calculate words</button>
            </div>

            { errorMessage.length ? <div className="Error"><span>{errorMessage}</span></div> : null }

            <div className="Histogram">
                { histogramData.length ?
                    <BarChart width={1200} height={500} data={histogramData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="frequency" fill="#8884d8" />
                    </BarChart> : null
                }
            </div>
        </div>
    )
}

export default App;
