import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button } from 'react-bootstrap';
import { useSearchParams } from 'react-router-dom';

function Home() {
    const [courses, setCourses] = useState([])
    const [q] = useSearchParams()

    useEffect(() => {
        console.info(Math.random())
        const loadCourses = async () => {
            const res = await fetch("/courses.json")
            let data = await res.json()

            let cateId = q.get("category_id")
            if (cateId !== null)
                data = data.filter(c => c.category_id == cateId)


            let kw = q.get("kw")
            if (kw !== null)
                data = data.filter(c => c.subject.indexOf(kw) >= 0)

            setCourses(data)
        }

        loadCourses()
    }, [q])

    return (
        <Container>
            <h1 className="text-center text-danger">DANH MUC KHOA HOC</h1>
            <Row>
                {courses.map(c => {
                    return <Item image={c.image} subject={c.subject} />
                })}
            </Row>
        </Container>
    )
}

const Item = (props) => {
    return (
        <Col md={4} xs={12}>
            <Card>
                <Card.Img variant="top" src={props.image} />
                <Card.Body>
                    <Card.Title>{props.subject}</Card.Title>
                    <Button variant="primary">Xem cac bai hoc</Button>
                </Card.Body>
            </Card>
        </Col>
    )
}

export default Home