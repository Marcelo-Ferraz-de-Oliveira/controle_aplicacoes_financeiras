import React from "react";
import { Container, Stack } from "react-bootstrap";
import styled from "styled-components";
const Layout = styled.div`
  stack {
    background-color: #fff;
    margin-top: 2px;
    margin-bottom: 2px;
    &:hover {
      background-color: #fff;
    }
  }
`;

const toBR = (str) => {
  return str.toLocaleString("pt-br", {
    minimumFractionDigits: 2,
  });
};

const Posicoes = ({ posicoes }) => {
  return (
    <Container className="bg-warning text-dark card p-3 justify-content-md-center">
      <h4>Posição atual</h4>
      {Object.values(posicoes).map((posicao) => (
        <Stack gap={2}>
          <Container fluid="sm" className="bg-light card p-1 px-3">
            <h6>Ativo: {posicao.ativo}</h6>
            <h6>Quantidade: {posicao.quantidade}</h6>
            <h6>Vencimento: {posicao.prazo}</h6>
            <h6>
              Preço médio: R$
              {toBR(posicao.preco_medio)}
            </h6>
            <h6>
              Valor: R$
              {toBR(posicao.valor)}
            </h6>
            {Object.entries(posicao.lucro).map(([data, lucro]) => (
              <h6>
                Lucro no dia {data}: {toBR(lucro)}
              </h6>
            ))}
          </Container>
        </Stack>
      ))}
    </Container>
  );
};

export default Posicoes;
