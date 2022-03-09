import React from "react";
import { Container, Card, ListGroup, Button } from "react-bootstrap";
import Section from "./Section";

const toBR = (str) => {
  return str.toLocaleString("pt-br", {
    minimumFractionDigits: 2,
  });
};

const Posicoes = ({ posicoes, liquitadeOption }) => {
  return (
    <Section bg="info" text="light" flex="lg">
      <Container className="row g-4">
        <h4 className="text-center">Posição atual</h4>
        {Object.values(posicoes).map((posicao) => (
          <Container className="col-md-6 col-lg-3" key={posicao.ativo}>
            <ListGroup>
              <ListGroup.Item>Ativo: {posicao.ativo}</ListGroup.Item>
              <ListGroup.Item>Quantidade: {posicao.quantidade}</ListGroup.Item>
              <ListGroup.Item>Vencimento: {posicao.prazo}</ListGroup.Item>
              <ListGroup.Item>
                Preço médio: R$
                {toBR(posicao.preco_medio)}
              </ListGroup.Item>
              <ListGroup.Item>
                Valor: R$
                {toBR(posicao.valor)}
              </ListGroup.Item>
              <ListGroup.Item>
                Expirado: {posicao.expirado === "true" ? "sim" : "não"}
              </ListGroup.Item>
              {posicao.expirado === "true" ? (
                <ListGroup.Item>
                  <Button
                    variant="primary"
                    onClick={() => liquitadeOption(posicao.ativo)}
                  >
                    Zerar Posição
                  </Button>
                </ListGroup.Item>
              ) : (
                <></>
              )}

              {Object.entries(posicao.lucro).map(([data, lucro]) => (
                <ListGroup.Item key={data}>
                  Lucro no dia {data}: {toBR(lucro)}
                </ListGroup.Item>
              ))}
            </ListGroup>
          </Container>
        ))}
      </Container>
    </Section>
  );
};

export default Posicoes;
