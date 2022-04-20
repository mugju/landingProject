import React from 'react';

import { BrowserRouter, Route, Routes, Link } from "react-router-dom";
import {Divider, List, ListItem, ListItemButton, ListItemText} from "@mui/material";

import "./SideMenuBar.css";

import Home from "../pages/Home";
import Company from "../pages/Company/Company";
import CompanyAccount from "../pages/CompanyAccount/CompanyAccount";
import Employee from "../pages/Employee/Employee";
import Medicine from "../pages/Medicine";
import Bill from "../pages/Bill";
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
                    <Link className="link" to="/company">
                        <ListItem button divider>
                            <ListItemText primary="Manage Company" />
                        </ListItem>
                    </Link>
                    <Link className="link" to="/companyAccount">
                        <ListItem button divider>
                            <ListItemText primary="Manage Company Account" />
                        </ListItem>
                    </Link>
                    <Link className="link" to="/employee">
                        <ListItem button divider>
                            <ListItemText primary="Manage Employee" />
                        </ListItem>
                    </Link>
                    <Link className="link" to="/medicine">
                        <ListItem button divider>
                            <ListItemText primary="Manage Medicine" />
                        </ListItem>
                    </Link>
                    <Link className="link" to="/bill">
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
                    <Route className="" path="/company" element={<Company/>} />
                    <Route className="" path="/companyAccount" element={<CompanyAccount/>} />
                    <Route className="" path="/employee" element={<Employee/>} />
                    <Route className="" path="/medicine" element={<Medicine/>} />
                    <Route className="" path="/bill" element={<Bill/>} />
                    <Route className="" path="/customerRequest" element={<CustomerRequest/>} />
                </Routes>

            </BrowserRouter>

        </>
    )
}