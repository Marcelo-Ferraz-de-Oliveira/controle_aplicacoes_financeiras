import React from "react";
import { useState, useEffect } from "react";
import Notas from "./packages/Notas";
import Loader from "./packages/Loader";
import { Container } from "react-bootstrap";
import { Layout } from "./packages/Layout";
import styled from "styled-components";

const App = () => {
  const [data, setData] = useState([]);

  const fetchData = async (body) => {
    const res = await fetch("/negocios", {
      method: "POST",
      body: body,
    });
    const content = await res.json();
    setData([...data, ...content]);

    //return content;
  };

  return (
    <Layout>
      <Container fluid="md">
        <Loader fetchData={fetchData} />
        {data.length === 0 ? "" : data && <Notas notas={data} />}
      </Container>
    </Layout>
  );
};

export default App;
