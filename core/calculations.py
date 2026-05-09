import math

import pandas as pd

from utils.types import Scalar
import utils.constants as c



def get_lambda(df: pd.DataFrame) -> tuple[Scalar, Scalar]:
    duration_with_no_internet_problems = 42 * 60

    total_arrivals = df.shape[0]

    LAMBDA = total_arrivals / duration_with_no_internet_problems

    se = df['Interval'].sem()

    return LAMBDA, se


def get_mu(df: pd.DataFrame) -> tuple[Scalar, Scalar]:
    mean_service_time = df.mean().iloc[0]

    MU = 1 / mean_service_time

    se = df.sem().iloc[0]

    return MU, se


def get_rho(lambda_, mu, c) -> Scalar:
    return lambda_ / (mu * c)


def get_p0(rho, c) -> Scalar:
    c_rho = c * rho
    summation: Scalar = 0

    for n in range(c):
        summation += (c_rho**n) / math.factorial(n)
        
    second_factor = (c_rho**c / math.factorial(c)) * (1 / (1 - rho))

    return 1 / (summation + second_factor)


def get_pi_w(rho, p0, c) -> Scalar:
    c_rho = c * rho
    pc = (c_rho**c / math.factorial(c)) * p0
    return pc / (1 - rho)


def get_Lq(rho, pi_w) -> Scalar:
    return pi_w * (rho / (1 - rho))


def get_Wq(mu, rho, pi_w, c) -> Scalar:
    return pi_w * (1 / (1 - rho)) * (1 / (c * mu))


def get_W(mu, Wq) -> Scalar:
    return Wq + (1 / mu)


def get_L(lambda_, W) -> Scalar:
    return lambda_ * W


def calibration(
        lambda_: Scalar, 
        mu: Scalar, 
        c_theoric: int, 
        slice_: slice = slice(None, None),
        columns: list[str] = ['Servidores', c.rho_char, 'Lq (pessoas)', 'W (segundos)']
) -> pd.DataFrame:
    parameter_list: list[Scalar] = []

    for n_servers in range(1, c_theoric + 1):
        rho = get_rho(lambda_, mu, n_servers)
        if rho > 1:
            continue
        p0 = get_p0(rho, n_servers)
        pi_w = get_pi_w(rho, p0, n_servers)
        Lq = get_Lq(rho, pi_w)
        Wq = get_Wq(mu, rho, pi_w, n_servers)
        W = get_W(mu, Wq)
        L = get_L(lambda_, W)
        
        parameter_list.append([n_servers, rho, Lq, W])

    df = pd.DataFrame(columns=columns, data=parameter_list).round(2)
    final_df = df.iloc[slice_]

    return final_df