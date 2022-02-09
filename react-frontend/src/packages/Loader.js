import React from "react";
import { Form, Button } from "react-bootstrap";
import { useState } from "react";
import styled from "styled-components";

const Layout = styled.div`
  .form {
    background-color: #222;
    &:hover {
      background-color: #333;
    }
  }
`;

const Loader = ({ fetchData }) => {
  const [file, setFile] = useState("");
  const [pwd, setPwd] = useState("");

  const onSubmit = (e) => {
    e.preventDefault();
    let data = new FormData();
    data.append("file", file);
    data.append("pwd", pwd);
    fetchData(data);
  };

  return (
    <Layout>
      <Form onSubmit={onSubmit}>
        <Form.Group className="mb-3" controlId="notadecorretagem">
          <Form.Label>Nota de corretagem</Form.Label>
          <Form.Control
            type="file"
            placeholder="Nota"
            onChange={(e) => setFile(e.target.files[0])}
          />
          <Form.Text className="text-muted"></Form.Text>
        </Form.Group>

        <Form.Group className="mb-3" controlId="password">
          <Form.Label>Senha</Form.Label>
          <Form.Control
            type="password"
            placeholder="Password"
            autoComplete="on"
            onChange={(e) => setPwd(e.target.value)}
          />
        </Form.Group>
        <Button variant="primary" type="submit">
          Processar nota de corretagem
        </Button>
      </Form>
    </Layout>
  );
};

export default Loader;
