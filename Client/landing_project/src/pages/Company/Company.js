import React, {useEffect, useState} from 'react';
import axios from 'axios';

import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

import Pagination from '@mui/material/Pagination';
import Button from "@mui/material/Button";
import {Box, IconButton, Modal, Typography, TextField, Tooltip, Divider} from "@mui/material";

import ClearIcon from '@mui/icons-material/Clear';


import AddCompany from './AddCompany';
import EditCompany from './EditCompany';
import ViewCompany from './ViewCompany';

import styles from './Company.module.css';


const URL = "http://localhost:5000/company/&page=";
const pageCount = 10;

export default function Company() {
    const [rows, setRows] = useState([]);
    const [bankList, setbankList] = useState([]);
    const [maxPage, setMaxPage] = useState(10);
    const [loading, setLoading] = useState(true);

    const [modalState, setModalState] = useState('view');
    const [modalOpen, setModalOpen] = useState(false);
    const [modalRow, setModalRow] = useState(0);

    const fetchUrl = async (URL, page) => {
        const response = await axios.get(URL + page);
        const resData = response.data;
        setRows(resData.company_list);
        setbankList(resData.bank_list);
        setMaxPage(Math.ceil(resData.companyallcount / pageCount))
        setLoading(false);
    }

    const openModal = (state, row) => {
        setModalRow(row);
        setModalState(state);
        setModalOpen(true);
    }

    const closeModal = () => {
        setModalOpen(false);
    }

    const selectModal = (state, row) => {
        if (state === 'add') {
            return <AddCompany
                bankList = {bankList}
                closeModal = {closeModal}
            />;
        } else if (state === 'view') {
            return <ViewCompany
                row = {row}
                setModalState = {setModalState}
                closeModal = {closeModal}
            />;
        } else if (state === 'edit') {
            return <EditCompany
                row = {row}
                closeModal = {closeModal}
            />;
        }
    }

    const handlePagi = (event, page) => {
        fetchUrl(URL, page);
    }

    useEffect(() => {
        fetchUrl(URL, 1);
    }, []);


    if (loading) {
        return null; // 로딩중 아이콘 넣기
    }

    return (
        <>
            <div className="innerContainer">
                <div className="titleContainer">
                    <div>All Companies</div>
                    <div>
                        <Button 
                            variant="contained" 
                            size="medium"
                            onClick={() => openModal('add')}
                        >
                            Add Company
                        </Button>
                    </div>
                </div>
                <TableContainer component={Paper}>
                    <Table sx={{width:'100%'}}>
                        <TableHead>
                            <TableRow>
                                <TableCell>No.</TableCell>
                                <TableCell>Name</TableCell>
                                <TableCell>License No.</TableCell>
                                <TableCell>Address</TableCell>
                                <TableCell>Contact No.</TableCell>
                                <TableCell>Email</TableCell>
                                <TableCell>Description</TableCell>
                                <TableCell>Added On</TableCell>
                                <TableCell>Action</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody className={styles.tableBody}>
                            {rows.map((row) => (
                                <TableRow
                                    key={row.com_uid}
                                >
                                    <TableCell component="th" scope="row">{row.com_uid}</TableCell>
                                    <TableCell><div>{row.com_name}</div></TableCell>
                                    <TableCell><div>{row.com_licence_no}</div></TableCell>
                                    <TableCell><div>{row.com_address}</div></TableCell>
                                    <TableCell><div>{row.com_contact_no}</div></TableCell>
                                    <TableCell><div>{row.com_email}</div></TableCell>
                                    <TableCell><div>{row.com_description}</div></TableCell>
                                    <TableCell><div>{row.com_joindate}</div></TableCell>
                                    <TableCell>
                                        <Button 
                                            variant="contained" 
                                            size="small" 
                                            onClick={() => openModal('view', row)}
                                        >
                                            View
                                        </Button>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>

                <Pagination className="pagination" count={maxPage} onChange={handlePagi} color="primary" />
                
            </div>

            <Modal
                className="modal"
                open={modalOpen}
                onClose={closeModal}
            >

                <>

                        {selectModal(modalState, modalRow)}

                </>
            </Modal>
        </>
    )
}