import Negocios from "./Negocios";
import { Container, Row, Stack } from "react-bootstrap";

const Notas = ({ notas }) => {
  return (
    <Container>
      {notas.map((nota) => (
        <Stack gap={2}>
          <Container className="justify-content-md-center border">
            <Container fluid="sm">
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
          </Container>

          <Negocios negocios={nota.Negocios} />
        </Stack>
      ))}
    </Container>
  );
};

export default Notas;
