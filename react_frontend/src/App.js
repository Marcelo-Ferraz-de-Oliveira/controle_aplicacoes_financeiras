import React from "react";
import { useState, useEffect } from "react";
import Notas from "./components/Notas";
import Loader from "./components/Loader";
import { Container } from "react-bootstrap";
import Posicoes from "./components/Posicoes";
import Profit from "./components/Profit";
import Header from "./components/Header";
import Footer from "./components/Footer";
import ModalError from "./components/ModalError";
import Section from "./components/Section";

const App = () => {
  const [data, setData] = useState([]);
  const [posicoes, setPosicoes] = useState([]);
  const [bText, setBText] = useState("Processar nota de negociação");
  const [profit, setProfit] = useState({});
  const [monthProfit, setMonthProfit] = useState(0);
  const [isError, setIsError] = useState("");

  useEffect(() => {
    //Fetch Tasks
    const fetchTasks = async () => {
      const res = await fetch("/posicao", {
        method: "POST",
      });
      const data = await res.json();
      console.log(data);
      setPosicoes(data);

      const resProfit = await fetch("/lucro", {
        method: "POST",
      });
      const jsonProfit = await resProfit.json();
      setProfit(jsonProfit);

      getMonthProfit();
    };
    fetchTasks();
  }, []);

  const fetchData = async (body) => {
    setBText("Processando...");
    const res = await fetch("/negocios", {
      method: "POST",
      body: body,
    });
    if (res && res.status === 200) {
      const content = await res.json();
      setData([...data, ...content]);
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
      updateProfit(content);
      getMonthProfit();
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
      console.log(content);
      setPosicoes(content);
      setData([]);
      updateProfit(content);
      getMonthProfit();
    } else {
      const error = await res.text();
      console.log(error);
      setIsError(error);
    }
  };

  const updateProfit = async (content) => {
    let profitForm = new FormData();
    profitForm.append("position", JSON.stringify(content));
    const profitRes = await fetch("/somarlucro", {
      method: "POST",
      body: profitForm,
    });
    const profitData = await profitRes.json();
    setProfit(profitData);
  };

  const getMonthProfit = async () => {
    const resMonthProfit = await fetch("/monthprofit", {
      method: "POST",
    });
    const jsonMonthProfit = await resMonthProfit.json();
    setMonthProfit(jsonMonthProfit);
  };

  return (
    <>
      <Header />
      <Loader fetchData={fetchData} bText={bText} />

      {profit.length === 0 ? (
        "Sem lucros"
      ) : (
        <Profit profit={profit} monthProfit={monthProfit} />
      )}

      {data.length === 0
        ? ""
        : data && <Notas notas={data} somarNotas={somarNotas} />}
      {posicoes.length === 0 ? (
        "Carregando posição..."
      ) : (
        <Posicoes posicoes={posicoes} liquitadeOption={liquidateOption} />
      )}
      <Section></Section>
      <Section></Section>
      <Footer />
      <ModalError error={isError} onHide={() => setIsError("")} />
    </>
  );
};

export default App;
