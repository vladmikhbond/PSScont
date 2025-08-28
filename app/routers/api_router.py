from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from .. import data_alch as db
from ..models.models import Problem, User
from ..models.schemas import ProofSchema, CheckSchema, ProblemPostSchema, ProblemSchema
from ..executors import js, py
import re

router = APIRouter()


# ============ Відкриті маршрути =============================

@router.post("/check")
async def post_check(schema: CheckSchema) -> str:
    """
    POST /api/check   \n
    Знаходить задачу, замінює авторське вирішення користувацьким,
    викликає post_proof()
    """
    problem = db.read_problem(schema.id)
    regex = regex_helper(problem.lang);
    if regex == None:
       return "Wrong Language" 
    newCode = re.sub(regex, schema.solving, problem.code, count=1, flags=re.DOTALL)
    return exec_helper(problem.lang, newCode, timeout=2)
     

@router.post("/proof")
async def post_proof(schema: ProofSchema) -> str:
    """
    POST /api/proof   \n
    Виконує програму, повертає повідомлення про результат.
    Повідомлення про позитивний результат починається з OK
    """
    return exec_helper(schema.lang, schema.source, timeout=2)
    
         
def regex_helper(lang:str):
    if lang == 'js':
        return r"//BEGIN.*//END"
    elif lang == 'py':
        return r"#BEGIN.*#END"
    else:
        return None


def exec_helper(lang:str, source: str, timeout: float):
    if lang == 'js':
        return js.exec(source, timeout=timeout)
    elif lang == 'py':
        return py.exec(source, timeout=timeout)
    else:
        return "Error: Unknown language"

# ============ Закриті маршрути =============================

from fastapi import Depends, HTTPException
from .token_router import get_current_user


AuthType = Annotated[str, Depends(get_current_user)]


@router.get("/reg/{username}", status_code=201)
async def register_user(username: str, user: AuthType):
    """
    Register a new student.
    """
    if user.role < 4:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not admin")    
    new_user = db.add_user(User(username=username, password="123456", role=1))
    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User exists")     
    return new_user;


# @router.get("/unreg/{username}")

# @router.get("/reset/{username}")


@router.get("/problems/lang/{lang}")
async def get_problems_lang(lang: str, user: AuthType) -> list[ProblemSchema]:
    """
    GET  /api/problems/lang/{lang}     \n
    Повертає задачі для заданої мови програмування.
    """
    problems: list[Problem] = db.read_problems_lang(lang)
    return problems 



@router.get("/problems/{id}")
async def get_problems_id(id: str, user: AuthType ) -> ProblemSchema:
    """
    GET  /api/problems/{id}     \n
    Повертає задачу з заданим id.
    """
    problem = db.read_problem(id) 
    if problem == None:
        raise HTTPException(status_code=404, detail=f"Error reading problem with id={id}")    
    return problem


@router.post("/problems")
async def post_problems(schema: ProblemPostSchema, user: AuthType) :
    """
    POST /api/problems     \n
    Перевіряє код і, якщо він годний, додає нову задачу в базу даних.
    """
    message = exec_helper(schema.lang, schema.code, timeout=2)
    if message.startswith("OK"):    
        problem = Problem(**schema.model_dump())
 
        added_problem = db.add_problem(problem)
        if added_problem is None:
            raise HTTPException(status_code=400, detail="Cannot add problem to DB")
        else:
            return added_problem.id
    else:
        raise HTTPException(status_code=400, detail=f"The code not checked. {message}")



@router.put("/problems")
async def put_problems(schema: ProblemSchema, user: AuthType):
    """
    PUT /api/problems    \n
    Перевіряє код і, якщо він годний, змінює задачу в базі даних.
    """
    message = exec_helper(schema.lang, schema.code, timeout=2)
    if message.startswith("OK"):          
        problem = Problem(**schema.model_dump())
        changed_problem = db.edit_problem(problem)
        if changed_problem is None:
            raise HTTPException(status_code=400, detail="The problem is not changed")
        else:
            return changed_problem.id
    else:
        raise HTTPException(status_code=400, detail=f"The code not checked. {message}")


@router.delete("/problems/{id}")
async def delete_problems_id(id: str, user: AuthType):
    """
    GET  /api/problems/{id}     \n
    Повертає видалену задачу або None.
    """
    problem = db.delete_problem(id) 
    if problem == None:
        raise HTTPException(status_code=400, detail=f"The problem with id = {id} is not deleted")   
    # problem_schema = ProblemSchema.model_validate(problem)
    return problem
