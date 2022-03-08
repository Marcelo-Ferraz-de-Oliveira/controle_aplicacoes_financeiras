import React from "react";
import { Form, Button } from "react-bootstrap";
import { useState } from "react";
import Section from "./Section";

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
    <Section bg="primary" text="light" flex="">
      <Form onSubmit={onSubmit}>
        <h4>Importar nota de negociação</h4>
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
        <Button variant="success" type="submit" size="lg">
          {bText}
        </Button>
      </Form>
    </Section>
  );
};

export default Loader;
