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
import Stack from '@mui/material/Stack';
import Button from "@mui/material/Button";
import {Box, IconButton, Modal, Typography, TextField, Tooltip, Divider} from "@mui/material";

import ClearIcon from '@mui/icons-material/Clear';
import DeleteForeverIcon from '@mui/icons-material/DeleteForever';

import AddCompany from './AddCompany';
import EditCompany from './EditCompany';
import ViewCompany from './ViewCompany';

import styles from './Company.module.css';


const URL = "https://4980c1be-d5e3-4906-a3a7-d989af4b993b.mock.pstmn.io/user";


export default function Company() {
    const [json, setJson] = useState([]);
    const [rows, setRows] = useState([]);
    const [loading, setLoading] = useState(true);
    const [rowCount, setRowCount] = useState(5);
    const [pageCount, setPageCount] = useState(10);

    const [modalPage, setModalPage] = useState('add');
    const [modalOpen, setModalOpen] = useState(false);
    const [modalNum, setModalNum] = useState(0);

    const fetchUrl = async (url) => {
        const response = await axios.get(url);
        const resData = response.data;
        setJson(resData);
        setRows(resData.slice(0, rowCount));
        setPageCount(Math.ceil(resData.length / rowCount));

        setLoading(false);
    }

    const openModal = (state, uid) => {
        setModalNum(uid);
        setModalPage(state);
        setModalOpen(true);
    }

    const closeModal = () => {
        setModalOpen(false);
    }

    const selectModal = (state, uid) => {
        if (state === 'add') {
            return <div>add</div>;
        } else if (state === 'view') {
            return <ViewCompany 
                uid = {uid}
                setModalPage = {setModalPage}
            />;
        } else if (state === 'edit') {
            return <EditCompany
                uid = {uid}
                closeModal = {closeModal}
            />;
        }
    }

    const handlePagi = (event, value) => {
        const first = value * rowCount - rowCount;
        const last = value * rowCount;
        const maxLen = json.length;

        setRows(json.slice(first, last > maxLen ? maxLen : last));
    }

    useEffect(() => {
        fetchUrl(URL);
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
                                    key={row.uid}
                                >
                                    <TableCell component="th" scope="row">{row.uid}</TableCell>
                                    <TableCell><div>{row.comName}</div></TableCell>
                                    <TableCell><div>{row.Licence_No}</div></TableCell>
                                    <TableCell><div>{row.address}</div></TableCell>
                                    <TableCell><div>{row.contact_No}</div></TableCell>
                                    <TableCell><div>{row.email}</div></TableCell>
                                    <TableCell><div>{row.description}</div></TableCell>
                                    <TableCell><div>{row.joinDate}</div></TableCell>
                                    <TableCell>
                                        <Button 
                                            variant="contained" 
                                            size="small" 
                                            onClick={() => openModal('view', row.uid)}
                                        >
                                            View
                                            </Button>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>

                <Pagination className="pagination" count={pageCount} onChange={handlePagi} color="primary" />
                {/* 페이지네이션 직접 구현해야될듯 */}
                
            </div>

            <Modal
                className="modal"
                open={modalOpen}
                onClose={closeModal}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <>
                    {selectModal(modalPage, modalNum)}

                </>
            </Modal>




{/* 
            <AddCompany />
            <ViewCompany />
            <EditCompany />
             */}


            {/* 모달별로 분리하기 */}


            {/* <Modal
                className="modal"
                open={open}
                onClose={closeModal}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <div className="modalContainer">
                    <div className="btnContainer">
                        <div className='deleteBtn'>
                            <Tooltip title="Delete">
                                <IconButton aria-label="close" className="iconBtn" onClick={() => console.log("delete")}>
                                    <DeleteForeverIcon />
                                </IconButton>
                            </Tooltip>
                        </div>
                        <div className='closeBtn'>
                            <Tooltip title="Close">
                                <IconButton aria-label="close" className="iconBtn" onClick={closeModal}>
                                    <ClearIcon />
                                </IconButton>
                            </Tooltip>
                        </div>
                    </div>
                    
                    {edit ? (
                        <>

                        </>
                    ) : (
                        <>

                        </>
                    )}

                </div>
            </Modal> */}





            {/* <Modal
                className="modal"
                open={open}
                onClose={closeModal}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            ></Modal> */}
        </>
    )
}