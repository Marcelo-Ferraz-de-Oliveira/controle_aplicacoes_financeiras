import React from "react";
import { useState, useEffect } from "react";
import Notas from "./components/Notas";
import Loader from "./components/Loader";
import { Container } from "react-bootstrap";
import { Layout } from "./components/Layout";
import styled from "styled-components";
import Posicoes from "./components/Posicoes";

const App = () => {
  const [data, setData] = useState([]);
  const [posicoes, setPosicoes] = useState([]);
  const [bText, setBText] = useState("Processar nota de negociação");
  const [cp, setCp] = useState({ Notas: true, Posicoes: true, Loader: true });

  useEffect(() => {
    //Fetch Tasks
    const fetchTasks = async () => {
      const res = await fetch("/posicao", {
        method: "POST",
      });
      const data = await res.json();
      setPosicoes(data);
    };
    fetchTasks();
  }, []);

  const fetchData = async (body) => {
    setBText("Processando...");
    const res = await fetch("/negocios", {
      method: "POST",
      body: body,
    });
    const content = await res.json();
    setData([...data, ...content]);
    setBText("Processar nota de negociação");
    //return content;
  };

  const somarNotas = async (notas) => {
    // alert(notas[0]["nr. nota"]);
    let data = new FormData();
    data.append("nota", JSON.stringify(notas));
    const res = await fetch("/somarnotas", {
      method: "POST",
      body: data,
    });
    const content = await res.json();
    setPosicoes(content);
    setData([]);
  };

  return (
    <Layout>
      <Container fluid="md" className=" mt-3 p-3">
        <Loader fetchData={fetchData} bText={bText} />
        {posicoes.length === 0 ? (
          "Carregando posição..."
        ) : (
          <Posicoes posicoes={posicoes} />
        )}
        {data.length === 0
          ? ""
          : data && <Notas notas={data} somarNotas={somarNotas} />}
      </Container>
    </Layout>
  );
};

export default App;
