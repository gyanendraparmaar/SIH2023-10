"use client";

import { useEffect, useState } from "react";
import { interpolateLab } from "d3-interpolate";
import Link from "next/link";

export default function Page() {
    const [departments, setDepartments] = useState([
      {dept: "Department for Promotion of Industry and Internal Trade"},
      {dept: "Department of Administrative Reforms and Public Grievances (DARPG)"},
      {dept: "Department of Agricultural Research and Education (DARE)"},
      {dept: "Department of Agriculture and Farmers Welfare"},
      {dept: "Department of Animal Husbandry and Dairying"},
      {dept: "Department of Biotechnology"},
      {dept: "Department of Border Management"},
      {dept: "Department of Chemicals and Petrochemicals"},
      {dept: "Department of Commerce"},
      {dept: "Department of Consumer Affairs"},
      {dept: "Department of Defence"},
      {dept: "Department of Defence Production"},
      {dept: "Department of Defence Research & Development"},
      {dept: "Department of Drinking Water and Sanitation"},
      {dept: "Department of Economic Affairs"},
      {dept: "Department of Empowerment of Persons with Disabilities"},
      {dept: "Department of Ex-Servicemen Welfare"},
      {dept: "Department of Expenditure"},
      {dept: "Department of Fertilizers"},
      {dept: "Department of Financial Services"},
      {dept: "Department of Fisheries"},
      {dept: "Department of Food and Public Distribution"},
      {dept: "Department of Health Research"},
      {dept: "Department of Health and Family Welfare"},
      {dept: "Department of Higher Education"},
      {dept: "Department of Home"},
      {dept: "Department of Investment and Public Asset Management"},
      {dept: "Department of Justice"},
      {dept: "Department of Land Resources (DLR)"},
      {dept: "Department of Legal Affairs"},
      {dept: "Department of Military Affairs (DMA)"},
      {dept: "Department of Official Language"},
      {dept: "Department of Pension & Pensioner's Welfare"},
      {dept: "Department of Personnel and Training"},
      {dept: "Department of Pharmaceuticals"},
      {dept: "Department of Posts"},
      {dept: "Department of Public Enterprises"},
      {dept: "Department of Revenue"},
      {dept: "Department of Rural Development (DRD)"},
      {dept: "Department of School Education and Literacy"},
      {dept: "Department of Science and Technology"},
      {dept: "Department of Scientific and Industrial Research"},
      {dept: "Department of Social Justice and Empowerment"},
      {dept: "Department of Sports"},
      {dept: "Department of Telecommunications"},
      {dept: "Department of Water Resources, River Development and Ganga Rejuvenation"},
      {dept: "Department of Youth Affairs"},
      {dept: "Inter-State Council Secretariat"},
      {dept: "Legislative Department"}
  ]);

    const [newsCards, setNewsCards] = useState([]);
    const [filteredNewsCards, setFilteredNewsCards] = useState([]);
    const [active, setActive] = useState(0);
    const [sentimentThreshold, setSentimentThreshold] = useState(0); 

    useEffect(() => {
      const getArticles = async () => {
        const res = await fetch("/api/articles", {
          method: "POST",
        });
        const resJson = await res.json();
        setNewsCards(resJson.data);
      }

      getArticles();
    }, [])

    useEffect(() => {
      setFilteredNewsCards(newsCards.filter(
          (card) => card.sentiment * 100 >= sentimentThreshold && card.department == departments[active].dept
      ));
    }, [newsCards, sentimentThreshold, departments])

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

    useEffect(() => {
        var dept = [...departments];
        dept[0].active = true;
        setDepartments(dept);
    }, []);

    return (
        <div className="min-h-full w-full bg-slate-100 grid grid-cols-5 gap-0">
            <div className="overflow-y-scroll h-screen">
                <div id="departments" className="bg-slate-700 h-fit col-span-1 flex flex-col gap-2 items-center justify-center">
                    <div className="top-0 mt-8 flex flex-col justify-center items-center gap-3 mb-10">
                        <p className="text-slate-300 font-bold text-2xl">DEPARTMENTS</p>
                        <hr className="border-2 border-slate-400 w-full"></hr>
                    </div>
                    {Object.keys(departments).map((i) => (
                        <div data-num={i} key={i} onClick={changeDept} className={`line-clamp-1 overflow-hidden text-ellipsis whitespace-nowrap cursor-pointer ${departments[parseInt(i)].active ? "rounded-r-none" : "rounded-full"} ${departments[parseInt(i)].active ? "hover:bg-slate-100" : "hover:bg-slate-600"} p-5 w-full text-center rounded-full ${departments[parseInt(i)].active ? "bg-slate-100" : "bg-transparent"} ${departments[parseInt(i)].active ? "text-slate-500" : "text-slate-300"} font-bold text-xl`}>
                            {departments[parseInt(i)].dept.replace("Department of", "").replace("Department for", "")}
                        </div>
                    ))}
                </div>
            </div>
            <div className="h-full col-span-4 flex flex-col items-center">
                <h1 className="text-4xl font-bold text-slate-700 m-5">
                    {departments[active].dept}
                </h1>
                <hr className="border-2 w-full"></hr>
                <div className="overflow-y-scroll h-screen">
                  <div className="h-fit w-full p-10 flex flex-wrap justify-center items-center gap-5">
                      { filteredNewsCards.map((card, i) => (<div key={i} className="relative w-96 h-96 p-5 rounded-md flex flex-col gap-1" style={{backgroundColor: `${interpolateLab("#ff7f69", "#a5ff69")(card.sentiment)}`}}>
                              <div className="text-center text-slate-700 text-base font-bold leading-6 max-h-12 overflow-hidden text-ellipsis line-clamp-2 mb-1">
                                  {card.title}
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
                                  {card.content}
                              </div>
                              <div
                                  className="absolute bottom-0 w-full h-16 -translate-x-5 backdrop-blur-sm rounded-md flex p-3 items-center justify-center"
                                  style={{ backgroundColor: "rgba(255, 255, 255, 0.2)" }}
                              >
                                  <p className="text-slate-700 absolute left-5">
                                      <span className="text-xl p-2">🙂</span>{" "}
                                      {(card.sentiment * 100).toFixed()}%
                                  </p>
                                  <Link href={`/article/${card.id}`} className="text-slate-600 font-bold">Analysis</Link>
                                  <Link target="_blank" href={card.link} className="absolute right-5 text-xl p-2">
                                      🔗
                                  </Link>
                              </div>
                          </div>
                          
                      ))}
                  </div>
                </div>
            </div>
            <div className="fixed bottom-10 right-10 backdrop-blur-md p-2 rounded-md" style={{ backgroundColor: "rgba(200, 200, 200, 0.5)" }}>
                <label htmlFor="sentimentThreshold" className="text-slate-700">
                    Sentiment Threshold:
                </label>
                <input
                    type="number"
                    id="sentimentThreshold"
                    value={sentimentThreshold}
                    step="1"
                    min="0"
                    max="100"
                    onChange={handleThresholdChange}
                    className="ml-2 px-2 py-1 border rounded-md outline-none w-16"
                />
            </div>
        </div>
    );
}
