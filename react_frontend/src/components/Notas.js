import Negocios from "./Negocios";
import Section from "./Section";

import { Container, Row, Stack, Button } from "react-bootstrap";

const Notas = ({ notas, somarNotas }) => {
  return (
    <Section>
      <Container fuid="sm">
        <h4>Notas de Negociação</h4>

        <Button
          className="btn btn-primary btn-lg btn-block"
          onClick={() => somarNotas(notas)}
        >
          Somar Nota
        </Button>
        {notas.map((nota) => (
          <Stack gap={2}>
            <Container fluid="sm" className="bg-light card p-2 px-1">
              <h6>Nome da Corretora: {nota.corretora}</h6>
              <h6>Data das operações: {nota.data}</h6>
              <h6>Número da nota: {nota.nota}</h6>
              <h6>Número da folha: {nota.folha}</h6>
              <h6>
                Custos das operações: R$
                {nota.custos.total.toLocaleString("pt-br", {
                  minimumFractionDigits: 2,
                })}
              </h6>
              <Negocios negocios={nota.negocios} />
            </Container>
          </Stack>
        ))}
      </Container>
    </Section>
  );
};

export default Notas;
