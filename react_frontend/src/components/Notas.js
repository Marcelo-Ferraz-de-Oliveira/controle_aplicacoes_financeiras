import Negocios from "./Negocios";
import Section from "./Section";

import { Container } from "react-bootstrap";

const Notas = ({ notas }) => {
  return (
    <Section>
      <Container fuid="sm">
        <h4>Notas de Negociação</h4>
        {notas.map((nota) => (
          <Container
            fluid="sm"
            className="bg-light card p-2 px-1 my-2"
            key={nota.nota}
          >
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
            <Negocios negocios={nota.negocios} numNota={nota.nota} />
          </Container>
        ))}
      </Container>
    </Section>
  );
};

export default Notas;
