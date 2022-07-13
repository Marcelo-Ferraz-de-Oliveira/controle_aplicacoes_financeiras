import React from "react";
import { useState, useEffect } from "react";
import Notas from "./components/Notas";
import Loader from "./components/Loader";
import Posicoes from "./components/Posicoes";
import Profit from "./components/Profit";
import Header from "./components/Header";
import Footer from "./components/Footer";
import ModalError from "./components/ModalError";
import ModalAbout from "./components/ModalAbout";

const App = () => {
  const [data, setData] = useState([]);
  const [posicoes, setPosicoes] = useState([]);
  const [bText, setBText] = useState("Processar nota de negociação");
  const [monthProfit, setMonthProfit] = useState(0);
  const [monthProfitDaytrade, setMonthProfitDaytrade] = useState(0);
  const [monthTax, setMonthTax] = useState(0);
  const [monthTaxDaytrade, setMonthTaxDaytrade] = useState(0);
  const [isError, setIsError] = useState("");
  const [showAbout, setShowAbout] = useState(true);

  useEffect(() => {
    //Fetch Tasks
    const fetchTasks = async () => {
      const res = await fetch("/posicao", {
        method: "POST",
      });
      const data = await res.json();
      setPosicoes(data);

      getMonthProfit();
      getMonthProfitDaytrade();
      getMonthTax();
      getMonthTaxDaytrade();
      fetchData();
    };
    fetchTasks();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchData = async (body = []) => {
    setBText("Processando...");
    const res = await fetch("/negocios", {
      method: "POST",
      body: body,
    });
    if (res && res.status === 200) {
      const content = await res.json();
      setData(content);
      somarNotas(content);
    } else {
      const error = await res.text();
      console.log(error);
      setIsError(error);
    }
    setBText("Processar nota de negociação");
  };

  const liquidateOption = async (code) => {
    let liquidateForm = new FormData();
    liquidateForm.append("code", JSON.stringify(code));
    const res = await fetch("/zerarposicao", {
      method: "POST",
      body: liquidateForm,
    });
    if (res && res.status === 200) {
      const content = await res.json();
      setPosicoes(content);
      getMonthProfit();
      getMonthProfitDaytrade();
      getMonthTax();
      getMonthTaxDaytrade();
    } else {
      const error = await res.text();
      console.log(error);
      setIsError(error);
    }
  };

  const somarNotas = async (notas) => {
    let data = new FormData();
    data.append("nota", JSON.stringify(notas));
    const res = await fetch("/somarnotas", {
      method: "POST",
      body: data,
    });
    if (res && res.status === 200) {
      const content = await res.json();
      setPosicoes(content);
      getMonthProfit();
      getMonthProfitDaytrade();
      getMonthTax();
      getMonthTaxDaytrade();
    } else {
      const error = await res.text();
      console.log(error);
      setIsError(error);
    }
  };

  const getMonthProfit = async () => {
    const resMonthProfit = await fetch("/monthprofit", {
      method: "POST",
    });
    const jsonMonthProfit = await resMonthProfit.json();
    setMonthProfit(jsonMonthProfit);
  };

  const getMonthProfitDaytrade = async () => {
    const resMonthProfitDaytrade = await fetch("/monthprofitdaytrade", {
      method: "POST",
    });
    const jsonMonthProfitDaytrade = await resMonthProfitDaytrade.json();
    setMonthProfitDaytrade(jsonMonthProfitDaytrade);
  };
  const getMonthTax = async () => {
    const resMonthTax = await fetch("/monthtax", {
      method: "POST",
    });
    const jsonMonthTax = await resMonthTax.json();
    setMonthTax(jsonMonthTax);
  };

  const getMonthTaxDaytrade = async () => {
    const resMonthTaxDaytrade = await fetch("/monthtaxdaytrade", {
      method: "POST",
    });
    const jsonMonthTaxDaytrade = await resMonthTaxDaytrade.json();
    setMonthTaxDaytrade(jsonMonthTaxDaytrade);
  };

  return (
    <div className="pb-5">
      <Header setShowAbout={setShowAbout} />
      <Loader fetchData={fetchData} bText={bText} />
      <Profit
        title="Resultados"
        monthProfit={monthProfit}
        monthTaxes={monthTax}
      />
      <Profit
        title="Resultados Day Trade"
        monthProfit={monthProfitDaytrade}
        monthTaxes={monthTaxDaytrade}
      />
      <Posicoes posicoes={posicoes} liquitadeOption={liquidateOption} />
      {data.length === 0 ? "" : data && <Notas notas={data} />}
      <Footer />
      <ModalError error={isError} onHide={() => setIsError("")} />
      <ModalAbout showAbout={showAbout} setShowAbout={setShowAbout} />
    </div>
  );
};

export default App;
