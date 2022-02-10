import Negocios from "./Negocios";
import { Container, Row, Stack, Button } from "react-bootstrap";

const Notas = ({ notas, somarNotas }) => {
  return (
    <Container className="bg-success card p-3">
      <h4 className="position-relative">Notas de Corretagem</h4>
      <Button className="my-2" onClick={() => somarNotas(notas)}>
        Somar nota
      </Button>
      {notas.map((nota) => (
        <Stack gap={2}>
          <Container fluid="sm" className="bg-light card p-2 px-1">
            <h6>Nome da Corretora: {nota.corretora}</h6>
            <h6>Data das operações: {nota.data}</h6>
            <h6>Número da nota: {nota["nr. nota"]}</h6>
            <h6>Número da folha: {nota.folha}</h6>
            <h6>
              Custos das operações: R$
              {nota.Custos.Total.toLocaleString("pt-br", {
                minimumFractionDigits: 2,
              })}
            </h6>
          </Container>

          <Negocios negocios={nota.Negocios} />
        </Stack>
      ))}
    </Container>
  );
};

export default Notas;
