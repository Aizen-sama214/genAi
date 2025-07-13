const fs = require('fs');
const path = require('path');


async function fetchJobData(jobId) {
    const jobDetailsResponse = await fetch(`https://www.instahyre.com/api/v1/anon_employer/413?jobId=${jobId}`, {
    "headers": {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
        "sec-ch-ua-arch": "\"arm\"",
        "sec-ch-ua-bitness": "\"64\"",
        "sec-ch-ua-full-version": "\"138.0.7204.93\"",
        "sec-ch-ua-full-version-list": "\"Not)A;Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"138.0.7204.93\", \"Google Chrome\";v=\"138.0.7204.93\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": "\"\"",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-ch-ua-platform-version": "\"15.5.0\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-csrftoken": "K0DaTNPwDl7CTIiGBEUCgu79RkZ1ZKYf8ELH9lLzc0YHn7HoYo9R2zjVAQlqHvog",
        "cookie": "csrftoken=K0DaTNPwDl7CTIiGBEUCgu79RkZ1ZKYf8ELH9lLzc0YHn7HoYo9R2zjVAQlqHvog; sessionid=mqdfuucfcn96pgue3rv5ijrv7mj0xzqa; _clck=uwus2d%7C2%7Cfxj%7C0%7C1572; _gid=GA1.2.334983277.1752321662; _ga_0PQL61K7YN=GS2.1.s1752321653$o94$g1$t1752321931$j60$l0$h0; _ga=GA1.2.1523442969.1713695843; _gat_UA-45611607-3=1",
        "Referer": "https://www.instahyre.com/candidate/opportunities/?matching=true&status=1"
    },
    "body": null,
    "method": "GET"
    });

    if (!jobDetailsResponse.ok) {
    throw new Error(`HTTP error! status: ${jobDetailsResponse.status}`);
    }   

    const jobDetails = await jobDetailsResponse.json();
    return jobDetails;
}

function getJobIds() {
    const dataDir = path.join(path.dirname(__dirname), 'data');
    const files = fs.readdirSync(dataDir);
    console.log(`Found ${files.length} job overview data files.`);
    const jobIds = []
    files.forEach(file => {
        if (!/^jobsOverviewData.*\.json$/.test(file)) return;
        console.log(`Processing file: ${file}`);
        const filePath = path.join(dataDir, file);
        const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
        data.objects.forEach(object => {
            if (object.job.id) {
                jobIds.push(object.job.id);
            }
        });
    });
    return jobIds;
}



async function main() {
    try {
        const jobIds = getJobIds();
        console.log(`Found ${jobIds.length} job IDs to fetch details for.`);
        const jobDetailsFilePath = path.join(path.dirname(__dirname), 'data/jobDetailsData.json');
        const jobDetailsFile = fs.readFileSync(jobDetailsFilePath);
        const jobDetailsData = JSON.parse(jobDetailsFile);
        let processedCount = 0;
        let failedCount = 0;
        for (const jobId of jobIds) {
            try{
                await new Promise(resolve => setTimeout(resolve, 10000)); // Delay to avoid hitting the server too hard
                const jobDetails = await fetchJobData(jobId);
                jobDetailsData.push(jobDetails);
                fs.writeFileSync(jobDetailsFilePath, JSON.stringify(jobDetailsData, null, 2));
                processedCount++;
            } catch (error) {
                failedCount++;
                console.error(`Error fetching job ${jobId} details:`, error);
            }
            console.log(`Status: ${processedCount} processed, ${failedCount} failed, ${jobIds.length - processedCount - failedCount} remaining`);
        }
    } catch (error) {
        console.error('Error fetching job details:', error);
    }
}

main();
