"use client";

import { useEffect, useState } from "react";
import { interpolateLab } from "d3-interpolate";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";

const newsCards = [
  {
    headline:
      "G20 technical workshop on 'Climate Resilient Agriculture' discusses scientific and innovative solutions",
    articleBody:
      "The G20 technical workshop on  Climate Resilient Agriculture  held here deliberated on issues related to climate resilient agriculture needs and innovations, case studies and experiences, policy, finance, and institutional needs for climate resilient agriculture. The Department of Agricultural Research and Education (DARE), Ministry of Agriculture and Farmers Welfare organised the workshop from September 4 to 6, which was attended by about 100 delegates including those from the G20 member states, invited countries, and international organisations, an official release said on Wednesday. Senior delegates from different countries and international organisations discussed technological, institutional and policy-related needs and imperatives. They also deliberated on scientific and innovative solutions that are required to address these emerging challenges to reduce the uncertainty in the agriculture food systems, it said. The concluding session was held under the chairmanship of SK Chaudhari, Deputy Director General (Natural Resource Management), Indian Council of Agricultural Research, who reiterated that by adopting climate-resilient crop varieties, managing the natural resources and imparting capacity building to the farmers and other stakeholders climate resilience can be achieved. He also explained the possibilities of adapting climate-resilient technologies in the G20 countries. The delegates from G20 countries expressed their views and opinions on climate-resilient practices, the release said. The officials explained that the adoption of climate resilient technologies are significant and can be upscaled by capacity building of the farmers and other stakeholders, it said. Senior officials from the Ministry of Agriculture and Jal Shakthi, Chemicals and Fertilizers, and Earth Sciences attended the meeting and presented their views on various issues of agriculture research pertaining to climate change in the global context, the release added.",
    sentiment: 0.2,
  },
  {
    headline:
      "Rural Development Ministry pushes for use of drones to monitor MNREGS work",
    articleBody:
      "In line with Centre's push for use of unmanned aerial vehicles in rural areas, especially in agriculture, the Rural Development Ministry has formulated a new policy for use of drones to monitor works under the Mahatma Gandhi NREGS. Drones will be used for monitoring ongoing work, inspection of completed work, and impact assessment. It can also be used by Ombudspersons appointed in each district to address grievances.  The expenditure towards using drones may be made under the Admin contingency component of the MNREGS, which is around 10 per cent of the fund allocated to the state.  No additional allocations have been made towards it and states have been directed to hire agencies specialising in using drone technology.   To leverage the use of drones, it has been proposed to use this technology for monitoring and inspection of works and quality of assets under Mahatma Gandhi NREGS,  the circular with the standard operating procedures said.  Drones will be used for monitoring works underway by capturing geo-referenced images before the start, during execution, and after the completion of the work.  Drones will also be used for gathering time series data for impact assessment of natural resource management, water and agriculture-related works done under the scheme.  Special inspections will also be carried out using drones, for enquiring complaints against the work or asset created, the circular said.  It will help Ombudspersons who are appointed in each district to receive grievances. The Ministry said Ombudsperson may also use drones for verification of the works virtually.   This facility will help Ombudsperson to pass awards in a bound manner. Therefore, the state government should provide drone facility to Ombudsperson for timely redress of complaints against a demand by the Ombudsperson,  the ministry said.  The quantum of the monitoring of works using drones may be decided by the states or Union Territories, it said.  The ministry in its SoPs has directed that drones being used should have a high-quality camera.  Users have also been asked to carry out the monitoring through drone in better light condition when the sun is overhead to minimise the shadows in photographs and it is also suggested to avoid partly cloudy days and high winds. The drone should be able to remain airborne for a minimum period of 30 minutes.  All videos and images through drone should be shared with the NREGA Soft.  Data generated over a period of time must be stored for comparison of time series data. The data can be used for systematic and scientific planning and monitoring of the rural area.  Addressing the nation from the ramparts of the Red Fort on the 77th Independence Day, Prime Minister Narendra Modi made a pitch for use of science and technology in rural development.  The PM said that 15,000 women's self-help groups would be given loan and training for operating and repairing drones.",
    sentiment: 0.72,
  },
];

export default function Page() {
  const [departments, setDepartments] = useState([
    {
      dept: "Personnel and Training",
    },
    {
      dept: "Legal Affairs",
    },
    {
      dept: "Commerce",
    },
    {
      dept: "Health",
    },
    {
      dept: "Food",
    },
    {
      dept: "Promotion of Industry",
    },
    {
      dept: "Sports",
    },
    {
      dept: "Science and Technology",
    },
    {
      dept: "ABCDEFGH",
    },
  ]);

  const [active, setActive] = useState(0);
  const [sentimentThreshold, setSentimentThreshold] = useState(100);

  const changeDept = (e) => {
    const dept = [...departments];
    dept[active].active = false;
    const next = e.target.getAttribute("data-num");
    dept[next].active = true;
    setActive(next);
    setDepartments(dept);
  };

  const handleThresholdChange = (e) => {
    const newThreshold = parseFloat(e.target.value);
    setSentimentThreshold(newThreshold);
  };
  const filteredNewsCards = newsCards.filter(
    (card) => card.sentiment * 100 <= sentimentThreshold
  );

  useEffect(() => {
    var dept = [...departments];
    dept[0].active = true;
    setDepartments(dept);
  }, []);

  return (
    <div className="min-h-full w-full bg-slate-100 grid grid-cols-5 gap-0">
      <div
        id="departments"
        className="bg-slate-700 h-full col-span-1 flex flex-col gap-1 items-center justify-center"
      >
        <div className="top-0 mt-8 flex flex-col justify-center items-center gap-3 mb-10">
          <p className="text-slate-300 font-bold text-2xl">DEPARTMENTS</p>
          <hr className="border-2 border-slate-400 w-full"></hr>
        </div>
        {Object.keys(departments).map((i) => (
          <div
            data-num={i}
            key={i}
            onClick={changeDept}
            className={`line-clamp-1 overflow-hidden text-ellipsis whitespace-nowrap cursor-pointer ${
              departments[parseInt(i)].active
                ? "rounded-r-none"
                : "rounded-full"
            } ${
              departments[parseInt(i)].active
                ? "hover:bg-slate-100"
                : "hover:bg-slate-600"
            } p-5 w-full text-center rounded-full ${
              departments[parseInt(i)].active
                ? "bg-slate-100"
                : "bg-transparent"
            } ${
              departments[parseInt(i)].active
                ? "text-slate-500"
                : "text-slate-300"
            } font-bold text-xl`}
          >
            {departments[parseInt(i)].dept}
          </div>
        ))}
      </div>
      <div className="h-full col-span-4 flex flex-col items-center">
        <h1 className="text-4xl font-bold text-slate-700 m-5">
          {departments[active].dept}
        </h1>
        <hr className="border-2 w-full"></hr>
        <div className="h-full w-full p-10 flex flex-wrap gap-5">
          {filteredNewsCards.map((card, i) => (
            <div
              key={i}
              className="relative w-96 h-96 p-5 rounded-md flex flex-col gap-1"
              style={{
                backgroundColor: `${interpolateLab(
                  "#ff7f69",
                  "#a5ff69"
                )(card.sentiment)}`,boxShadow: "0 10px 10px rgba(0, 0, 0, 0.5)"
              }}
            >
              <div className="text-center text-slate-700 text-base font-bold leading-6 max-h-12 overflow-hidden text-ellipsis line-clamp-2 mb-1">
                {newsCards[i].headline}
              </div>
              <hr className="w-full border-1 border-slate-100"></hr>
              <div
                className="relative h-48 text-slate-700 overflow-hidden text-ellipsis tracking-wide m-3"
                style={{
                  overflow: "hidden",
                  display: "-webkit-box",
                  WebkitBoxOrient: "vertical",
                  WebkitLineClamp: "8",
                }}
              >
                {newsCards[i].articleBody}
              </div>
              <div
                className="absolute bottom-0 w-full h-16 -translate-x-5 backdrop-blur-sm cursor-pointer rounded-md flex p-3 items-center"
                style={{ backgroundColor: "rgba(255, 255, 255, 0.2)" }}
              >
                <p className="text-slate-700">
                  <span className="text-xl p-2">🙂</span>{" "}
                  {newsCards[i].sentiment * 100}%
                </p>
                <a
                  href={`/article/${i}`}
                  className="text-xl p-2"
                  style={{ marginLeft: "200px" }}
                >
                  🔗
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>
      <div className="fixed bottom-10 right-10">
        <label htmlFor="sentimentThreshold" className="text-slate-700">
          Sentiment Threshold:
        </label>
        <input
          type="number"
          id="sentimentThreshold"
          value={sentimentThreshold}
          step="0.01"
          min="0"
          max="1"
          onChange={handleThresholdChange}
          className="ml-2 px-2 py-1 border rounded-md"
        />
      </div>
    </div>
  );
}
