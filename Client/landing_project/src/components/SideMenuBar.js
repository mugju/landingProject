import React from 'react';

import { BrowserRouter, Route, Routes, Link } from "react-router-dom";
import {Divider, List, ListItem, ListItemButton, ListItemText} from "@mui/material";

import "./SideMenuBar.css";

import Home from "../pages/Home";
import ManageCompany from "../pages/ManageCompany";
import ManageCompanyAccount from "../pages/ManageCompanyAccount";
import ManageEmployee from "../pages/ManageEmployee";
import ManageMedicine from "../pages/ManageMedicine";
import GenerateBill from "../pages/GenerateBill";
import CustomerRequest from "../pages/CustomerRequest";




export default function SideMenuBar() {
    return (
        <>

            <BrowserRouter>
                <List className="sideNav" component="nav" aria-label="mailbox folders">
                    <Link className="link" to="/">
                        <ListItem button divider>
                            <ListItemText primary="Home" />
                        </ListItem>
                    </Link>
                    <Link className="link" to="/manageCompany">
                        <ListItem button divider>
                            <ListItemText primary="Manage Company" />
                        </ListItem>
                    </Link>
                    <Link className="link" to="/manageCompanyAccount">
                        <ListItem button divider>
                            <ListItemText primary="Manage Company Account" />
                        </ListItem>
                    </Link>
                    <Link className="link" to="/manageEmployee">
                        <ListItem button divider>
                            <ListItemText primary="Manage Employee" />
                        </ListItem>
                    </Link>
                    <Link className="link" to="/manageMedicine">
                        <ListItem button divider>
                            <ListItemText primary="Manage Medicine" />
                        </ListItem>
                    </Link>
                    <Link className="link" to="/generateBill">
                        <ListItem button divider>
                            <ListItemText primary="Generate Bill" />
                        </ListItem>
                    </Link>
                    <Link className="link" to="/customerRequest">
                        <ListItem button divider>
                            <ListItemText primary="Customer Request" />
                        </ListItem>
                    </Link>
                </List>

                <Routes>
                    <Route className="" path="/" element={<Home/>} />
                    <Route className="" path="/manageCompany" element={<ManageCompany/>} />
                    <Route className="" path="/manageCompanyAccount" element={<ManageCompanyAccount/>} />
                    <Route className="" path="/manageEmployee" element={<ManageEmployee/>} />
                    <Route className="" path="/manageMedicine" element={<ManageMedicine/>} />
                    <Route className="" path="/generateBill" element={<GenerateBill/>} />
                    <Route className="" path="/customerRequest" element={<CustomerRequest/>} />
                </Routes>

            </BrowserRouter>

        </>
    )
}