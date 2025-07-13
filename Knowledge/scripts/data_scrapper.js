const fs = require('fs');
const path = require('path');

async function fetchJobData(page = 1) {
    const jobdataresponse = await fetch(
        `https://www.instahyre.com/api/v1/candidate_opportunity?company_size=&industry_type=&interest_facet=1&job_type=&limit=30&location=&offset=${(page - 1) * 30}`, 
        {
            "headers": {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
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
            "cookie": "csrftoken=K0DaTNPwDl7CTIiGBEUCgu79RkZ1ZKYf8ELH9lLzc0YHn7HoYo9R2zjVAQlqHvog; sessionid=mqdfuucfcn96pgue3rv5ijrv7mj0xzqa; _clck=uwus2d%7C2%7Cfxj%7C0%7C1572; _gid=GA1.2.334983277.1752321662; _ga_0PQL61K7YN=GS2.1.s1752321653$o94$g1$t1752321678$j35$l0$h0; _ga=GA1.1.1523442969.1713695843",
            "Referer": "https://www.instahyre.com/candidate/opportunities/?matching=true&status=1"
        },
        "body": null,
        "method": "GET"
    });

    if (!jobdataresponse.ok) {
        throw new Error(`HTTP error! status: ${jobdataresponse.status}`);
    }   

    const jobdata = await jobdataresponse.json();

    const outputPath = path.join(path.dirname(__dirname), `data/jobsOverviewData${page-1}.json`);

    fs.writeFileSync(outputPath, JSON.stringify(jobdata, null, 2), 'utf-8');

}

async function main() {
  try {
    console.log(`The job is running in dir ${__dirname}`)
    for (let i = 1; i <= 11; i++) {
      await fetchJobData(i);
      await new Promise(resolve => setTimeout(resolve, 15000)); // Delay to avoid hitting the server too hard
      console.log(`Job data for page ${i} fetched and saved.`);
    }
  } catch (error) {
    console.error('Error fetching job data:', error);
  }
}

main();