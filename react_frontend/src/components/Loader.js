import React from "react";
import { Form, Button } from "react-bootstrap";
import { useState } from "react";
import styled from "styled-components";

const Layout = styled.div`
  form {
    background-color: #fff;
    margin-top: 2px;
    margin-bottom: 2px;
    &:hover {
      background-color: #fff;
    }
  }
`;

const Loader = ({ fetchData, bText }) => {
  const [files, setFiles] = useState("");
  const [pwd, setPwd] = useState("");

  const onSubmit = (e) => {
    e.preventDefault();
    let data = new FormData();
    let x = 0;
    for (let file of files) {
      data.append(`file${x}`, file);
      x++;
    }
    data.append("pwd", pwd);
    fetchData(data);
  };

  return (
    <Layout className="bg-light card p-3">
      <h4>Importar nota de negociação</h4>
      <Form onSubmit={onSubmit} className="d-grid bg-light">
        <Form.Group className="mb-3" controlId="notadecorretagem">
          <Form.Label>Nota de negociação (PDF)</Form.Label>
          <Form.Control
            type="file"
            multiple
            placeholder="Nota"
            onChange={(e) => setFiles(e.target.files)}
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
        <Button variant="primary" type="submit" size="lg">
          {bText}
        </Button>
      </Form>
    </Layout>
  );
};

export default Loader;
