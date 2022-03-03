import Negocios from "./Negocios";
import { Container, Row, Stack, Button } from "react-bootstrap";

const Notas = ({ notas, somarNotas }) => {
  return (
    <Container className="bg-success card p-3">
      <h4 className="position-relative">Notas de Negociação</h4>
      <Button className="my-2" onClick={() => somarNotas(notas)}>
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
          </Container>

          <Negocios negocios={nota.negocios} />
        </Stack>
      ))}
    </Container>
  );
};

export default Notas;
