import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from "react-router-dom"
import { Navbar, Nav, Form, FormControl, Button } from 'react-bootstrap';

function Header() {
    const [categories, setCategories] = useState([])
    const [kw, setKw] = useState("")
    const nav = useNavigate()

    useEffect(() => {
        let loadCategories = async () => {
            let res = await fetch("/categories.json")
            let data = await res.json()
            setCategories(data)
        }

        loadCategories()
    }, [])

    const search = (event) => {
        event.preventDefault()

        nav(`/?kw=${kw}`)
    }

    return (
        <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
            <Navbar.Brand href="#home">React-Bootstrap</Navbar.Brand>
            <Navbar.Toggle aria-controls="responsive-navbar-nav" />
            <Navbar.Collapse id="responsive-navbar-nav">
                <Nav className="me-auto">
                    {categories.map(c => {
                        const url = `/?category_id=${c.id}`
                        return <Link to={url} className="nav-link">{c.name}</Link>
                    })}
                </Nav>
                <Form className="d-flex" onSubmit={search}>
                    <FormControl
                        type="search"
                        value={kw}
                        onChange={event => setKw(event.target.value)}
                        placeholder="Tu khoa..."
                        className="me-2"
                        aria-label="Search"
                    />
                    <Button type="submit" variant="outline-success">Tim</Button>
                </Form>
            </Navbar.Collapse>
        </Navbar>
    )
}

export default Header